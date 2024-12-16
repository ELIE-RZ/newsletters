from django.urls import include, path

from .import views
from .views import (
    Register, Home, Login, PostLetter, Facultes, Delete, UpdateProfil,
    Departement, Index, Logout, Forum, Contact, LsitPub, Modify, UserList,
    InboxMessage,
    )

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('view/', views.Myview.as_view()),
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('home/', Home.as_view(), name="home"),
    path('post/', PostLetter.as_view(), name="post"),
    path('faculty/', Facultes.as_view(), name="faculty"),
    path('departement/', Departement.as_view(), name="department"),
    path('forum/', Forum.as_view(), name='forum'),
    path('contact/', Contact.as_view(), name='contact'),
    path('listpubs/', LsitPub.as_view(), name='listpubs'),
    path("modify/<int:pk>", Modify.as_view(), name="modify"),
    path('delete/<int:pk>', Delete.as_view(), name='delete'),
    path("profilupdate/<int:pk>", UpdateProfil.as_view(), name='profilupdate'),
    path('userlist/', UserList.as_view(), name='userlist'),
    path('messages/<int:pk>', InboxMessage.as_view(), name='messages')
]

