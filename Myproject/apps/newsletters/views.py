from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .models import CustomUser, Departements, Faculty, Messages, Notification, Posteletters
from .forms import RegisterForm, LoginForm, PostForm, FacultyForm, DepartementForm


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
            return redirect("home")
        return render(request, self.template_name, {"forms":forms})


class Login(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        forms = self.template_name(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, "Vous êtes conneté")
                return redirect("home")
        return render(request, "connect.html", {"form": forms})
       
class Logout(LogoutView):
    def get(self, request):
        logout(request)
        return redirect(reverse("connexion"))


class PostLetter(View):
    template_name = "poste.html"
    model = Posteletters
    form_class = PostForm
    initial = {"key":"value"}

    def get(self, request):
        forms = self.form_class(initial = self.initial)
        return render(request, self.template_name, {"forms":forms})
    
    def post(self, request):
        forms = self.template_name(request.POST, request.FILES)
        if forms.is_valid():
            object = forms.save(commit = False)
            object.created_by = request.user
            object.save()
            Notification.objects.create(
                created_by=request.user, notification="Vous avez publier une lettre d'information."
            )
            messages.success(request, "Votre publication a été créée avec succes.")
            return redirect("/")
        else:
            forms = PostForm()
            messages.error(request, "une erreur s'est produit")
        return render(request, self.template_name, {"forms": forms})
    

class Facutes(View):
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


class Departement(View):
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


class Home(TemplateView):
    template_name = "home.html"

class Index(TemplateView):
    template_name = "index.html"
"""List Views"""


def get_departments(request):
    faculty_id = request.GET.get('faculty_id')
    if faculty_id:
        try:
            faculty = Faculty.objects.get(id=faculty_id)
            departments = Departements.objects.filter(faculty=faculty)
            data = [{"id": dept.id, "name": dept.departement} for dept in departments]
            return JsonResponse(data, safe=False)
        except Faculty.DoesNotExist:
            return JsonResponse({"error": "Faculty not found"}, status=404)
    return JsonResponse({"error": "Faculty ID not provided"}, status=400)