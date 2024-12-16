from django.db import models
from django.contrib.auth.models import AbstractUser
from Myproject.apps.core.models import Post
from django.utils.translation import gettext as _
from django.utils.timezone import now


# Create your models here.
class CustomUser(AbstractUser):
    class Nationality(models.TextChoices):
        DRC = "DRC", _("Congolaise")
        BURUNDI = "Bu", _("Burundaise")
        TANZANIA= "Tz", _("Tanzanienne")
        AUTRE = "A", _("autres")

    nationality = models.CharField(max_length=120, choices=Nationality, default=Nationality.AUTRE)
    fonction = models.CharField(max_length=250)
    profil = models.ImageField(upload_to= "images/", null=True, blank=True)

    def __str__(self):
        return self.username
    
class Faculty(models.Model):
    class Fac(models.TextChoices):
        TECHNOLOGIES = "FIT", _("Facultés d'Ingénierie et de Technologie")
        LETTRE = "FLS", _("Facutés des Lettres et des Sciences")
        EDUCATION = "FE", _("Facultés de l'Educations")
        SANTÉ = "FSS", _("Facultés des Sciences de la Santé")
        AFFAIRES = "FSAP", _("Facultés des Sciences et des Affaires Proffessionnelles")
        MEDECINE = "FM", _("Faculté de Medecine")
        AUTRE = "A", _("Autre")

    user = models.ForeignKey("CustomUser", on_delete = models.DO_NOTHING, related_name="faculte")
    faculty = models.CharField(max_length=250, choices=Fac.choices, default=Fac.AUTRE)

class Departements(models.Model):
    class DeptChoices(models.TextChoices):
        # Exemples de départements par faculté
        INFORMATIQUE = "INFO", _("Informatique")
        ELECTRONIQUE = "ELEC", _("Électronique")
        LITTERATURE = "LITT", _("Littérature")
        PHILOSOPHIE = "PHILO", _("Philosophie")
        PEDAGOGIE = "PEDA", _("Pédagogie")
        MEDECINE_GENERALE = "MEDG", _("Médecine Générale")
        PHARMACIE = "PHAR", _("Pharmacie")
        GESTION = "GEST", _("Gestion")
        MARKETING = "MARK", _("Marketing")

    faculty = models.ForeignKey("Faculty",on_delete=models.CASCADE, related_name="departement")
    departement = models.CharField(max_length=250, choices=DeptChoices.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.departement


class Posteletters(Post):
    title = models.CharField(max_length=250)
    discription = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to= "images/", null=True, blank=True)
    fichier = models.FileField(upload_to= "images/", null=True, blank=True)


class Messages(Post):
    message = models.TextField()
    is_read = models.BooleanField(default=False)


class Notification(Post):
    notification = models.TextField()
    is_read = models.BooleanField(default=False)


# class Message(models.Model):
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     content = models.TextField(blank=True, null=True)
#     reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Message from {self.sender.username} in {self.conversation}"
    

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"