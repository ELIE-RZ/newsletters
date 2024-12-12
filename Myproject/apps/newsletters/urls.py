from django.urls import include, path

from .import views
from .views import (Register, Home, Login, PostLetter, Facutes, Departement, Index, Logout)

urlpatterns = [
    path('', views.bonjour),
    path('view/', views.Myview.as_view()),
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('home/', Home.as_view(), name="home"),
    path('post/', PostLetter.as_view(), name="post"),
    path('faculty/', Facutes.as_view(), name="faculty"),
    path('departement/', Departement.as_view(), name="department"),
    path('index/', Index.as_view(), name='index'),
]
