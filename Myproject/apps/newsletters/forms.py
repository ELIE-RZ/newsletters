from django import forms
from .models import CustomUser, Posteletters, Messages, Notification, Departements, Faculty
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "nationality", "fonction", "profil"]


class ProfilUpdate(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "profil"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email d'utilisateur"}),
        "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class PostForm(forms.ModelForm):
    class Meta:
        model = Posteletters
        fields = ["title", "discription", "image", "fichier"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre titre"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Votre description"}),
            "image": forms.FileInput(),
            "fichier": forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class Modifyletters(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre titre"}),
    )
    discription = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Votre description"})
    )
    picture = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control"}))
    fichier = forms.FileField(widget=forms.FileInput)

    class Meta:
        model = Posteletters
        fields = ["title", "discription", "picture", "fichier"]

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ["faculty"]


# class DepartementForm(forms.ModelForm):
#     class Meta:
#         model = Departements
#         fields = ['faculty', 'departement']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  # Obtenez l'utilisateur
#         super().__init__(*args, **kwargs)

#         if user:
#             """Filtrer les facultés pour l'utilisateur courant"""
#             self.fields['faculty'].queryset = Faculty.objects.filter(user=user)

#             """Filtrer les départements selon la faculté sélectionnée"""
#             if 'faculty' in self.data:
#                 try:
#                     faculty_id = int(self.data.get('faculty'))
#                     self.fields['departement'].queryset = Departements.objects.filter(faculty_id=faculty_id)
#                 except (ValueError, TypeError):
#                     self.fields['departement'].queryset = Departements.objects.none()
#             elif self.instance.pk:
#                 self.fields['departement'].queryset = self.instance.faculty.departements.all()



class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departements
        fields = ['faculty', 'departement']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                # Logique pour filtrer les choix de départements selon la faculté
                faculty = Faculty.objects.get(id=faculty_id)
                if faculty.faculty == Faculty.Fac.TECHNOLOGIES:
                    self.fields['departement'].choices = [
                        choice for choice in Departements.DeptChoices.choices if choice[0] in ['INFO', 'ELEC']
                    ]
                elif faculty.faculty == Faculty.Fac.LETTRE:
                    self.fields['departement'].choices = [
                        choice for choice in Departements.DeptChoices.choices if choice[0] in ['LITT', 'PHILO']
                    ]
                elif faculty.faculty == Faculty.Fac.MEDECINE:
                    self.fields['departement'].choices = [
                        choice for choice in Departements.DeptChoices.choices if choice[0] in ['MEDG', 'PHAR']
                    ]
                # Ajoutez des conditions pour les autres facultés ici
                else:
                    self.fields['departement'].choices = Departements.DeptChoices.choices  # Par défaut, tous les choix
            except (ValueError, Faculty.DoesNotExist):
                self.fields['departement'].choices = []
