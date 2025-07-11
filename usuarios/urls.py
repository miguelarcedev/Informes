# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('activar/<uidb64>/<token>/', views.activar, name='activar'),
]
