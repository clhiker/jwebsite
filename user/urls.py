from django.urls import path
from . import views

urlpatterns = [
    path('login.html',    views.login,    name='login'),
    path('register.html', views.register, name='register'),
    path('',              views.logout,   name='logout'),
]

