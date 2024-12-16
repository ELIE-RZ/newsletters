from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q

from .models import CustomUser, Departements, Faculty, Messages, Notification, Posteletters, Message
from .forms import (RegisterForm, LoginForm, PostForm,  ProfilUpdate, MessagesForm,
                    FacultyForm, DepartementForm, MessageForm, Modifyletters)


# Create your views here.

def bonjour(request):
    return HttpResponse('bonjour à tous')

class Myview(View):
    def get(self, request):
        return render('myview')


"""Les Vues des Formulaires"""

class Register(View):
    template_name = "Inscription.html"
    form_class = RegisterForm
    initial = {"key":"value"}

    def get(self, request):
        forms = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"forms": forms})
    
    def post(self, request):
        forms = self.form_class(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect("")
        return render(request, self.template_name, {"forms":forms})


class Login(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        forms = self.form_class(request.POST, request.FILES)

        if forms.is_valid():
            username = forms.cleaned_data["username"]
            password = forms.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, "Vous êtes conneté")
                return redirect("home")
        return render(request, "connect.html", {"form": forms})
            
       
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("login"))


class PostLetter(LoginRequiredMixin, View):
    template_name = "poste.html"
    model = Posteletters
    form_class = PostForm
    initial = {"key":"value"}

    def get(self, request):
        forms = self.form_class(initial = self.initial)
        return render(request, self.template_name, {"forms":forms})
    
    
    def post(self, request):
        if request.method == 'POST':
            forms = self.form_class(request.POST, request.FILES)
            if forms.is_valid():
                objet = forms.save(commit=False)
                objet.created_by = request.user
                objet.save()
                objet.created_by = request.user
                objet.save()
                Notification.objects.create(
                    created_by=request.user, notification="Vous avez publier une lettre d'information."
                )
                messages.success(request, "Votre publication a été créée avec succes.")
                return redirect("home")
            else:
                forms = PostForm()
                messages.error(request, "une erreur s'est produit")
        return render(request, self.template_name, {"forms": forms})
    

class Facultes(LoginRequiredMixin, View):
    template_name = "home.html"
    form_class = FacultyForm
    model = Faculty
    initial = {"key":"value"}

    def get(self, request):
        forms = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"forms":forms})
    
    def post(self, request):
        forms = self.template_name(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success("vous alors déja la faculté")
            return redirect("faculty")
        return render(request, self.template_name, {"forms":forms})


class Departement(LoginRequiredMixin, View):
    template_name = "home.html"
    form_class = DepartementForm
    model = Faculty
    initial = {"key":"value"}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form":form})
    
    def post(self, request):
        form = self.template_name(request.POST)
        if form.is_valid():
            form.save()
            messages.success("vous avez choisi la faculté")
            return redirect("home")
        return render(request, self.template_name, {"form":form})


class Home(LoginRequiredMixin, View):
    def get(self, request):
        if request.method == "GET":
            postes = Posteletters.objects.all().order_by('-created_at')
            return render(request, "home.html", {"postes": postes})


class Index(TemplateView):
    template_name = "index.html"
"""List Views"""


class LsitPub(LoginRequiredMixin, View):
    template_name = "listpub.html"
    model = Posteletters
    def get(self, request):
        if request.method == "GET":
            pubs = self.model.objects.all().filter(created_by=self.request.user)
            return render(request, self.template_name, {"pubs":pubs})


class Modify(LoginRequiredMixin, UpdateView):
    model = Posteletters
    template_name = "modifypub.html"
    form_class =Modifyletters

    def post(self, request, pk):
        if request.method == 'POST':
            objet = self.model.objects.get(pk=pk)
            forms = self.form_class(request.POST, request.FILES or None, instance=objet)
            if forms.is_valid():
                forms.save()
                return redirect("listpubs")
        return render(request, self.template_name, {"form": forms})


class UpdateProfil(LoginRequiredMixin, UpdateView):
    template_name = "changeprofil.html"
    model = CustomUser
    form_class = ProfilUpdate

    def post(self, request, pk):
        if request.method == 'POST':
            object = self.model.objects.get(pk=pk)
            forms = self.form_class(request.POST, request.FILES or None, instance=object)
            if forms.is_valid():
                forms.save()
                return redirect("listpubs")
        return render(request, self.template_name, {"form":forms})


class Delete(LoginRequiredMixin, DeleteView):
    model = Posteletters

    def get(self, request, pk):
        objet = self.model.objects.get(pk=pk)
        objet.delete()
        return redirect("listpubs")


class Contact(TemplateView):
    template_name = "contact.html"


class Forum(LoginRequiredMixin, View):
    template_name = "forum.html"
    model = Messages
    form_class = MessagesForm
    initial = {"key": "value"}

    def get(self, request):
        forms = self.form_class(initial=self.initial)
        messages = self.model.objects.all().order_by('-created_at')  # Trier par date décroissante
        return render(request, self.template_name, {"forms": forms, "messages": messages})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            objet = forms.save(commit=False)
            objet.created_by = request.user  # Associer l'utilisateur
            objet.save()
            return redirect('forum')  # Rediriger vers la même page pour voir les nouveaux messages
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez réessayer.")
        messages = self.model.objects.all().order_by('-created_at')
        return render(request, self.template_name, {"forms": forms, "messages": messages})
    
    
class UserList(LoginRequiredMixin, View):
    template_name = 'userlist.html'
    model = CustomUser

    def get(self, request):
        utilisateurs = self.model.objects.all()
        return render(request, self.template_name, {"users":utilisateurs})


class InboxMessage(LoginRequiredMixin, View):
    template_name = "message.html"
    form_class = MessageForm

    def get(self, request, pk):
        """
        Récupère la conversation entre l'utilisateur actuel et un autre utilisateur.
        """
        other_user = get_object_or_404(CustomUser, pk=pk)
        messages = Message.objects.filter(
            sender=request.user, receiver=other_user
        ) | Message.objects.filter(
            sender=other_user, receiver=request.user
        ).order_by('timestamp')
        
        form = self.form_class(initial={'receiver': other_user})
        return render(request, self.template_name, {
            'messages': messages, 'other_user': other_user, 'form': form
        })

    def post(self, request, pk):
        """
        Traite un nouveau message envoyé par l'utilisateur actuel.
        """
        other_user = get_object_or_404(CustomUser, pk=pk)
        form = self.form_class(request.POST)
        
        if form.is_valid():
            
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('messages', pk=pk)
        
        
        messages = Message.objects.filter(
            sender=request.user, receiver=other_user
        ) | Message.objects.filter(
            sender=other_user, receiver=request.user
        ).order_by('timestamp')
        
        return render(
            request, self.template_name, {'messages': messages, 'other_user': other_user, 'form': form
        })
