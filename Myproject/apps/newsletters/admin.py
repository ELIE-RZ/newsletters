from django.contrib import admin

from .models import CustomUser, Posteletters


# Classe d'administration pour le modèle CustomUser
class TableUsersAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "password"]


# Enregistrement du modèle avec la classe d'administration
admin.site.register(CustomUser)
admin.site.register(Posteletters)

