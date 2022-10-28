from django.contrib import admin
from django.urls import path
from . import views

from publicador.views import Tarjeta, ActivosListView, InactivosListView, Tarjeta_Inactivo,Irregulares,Publicador_list



urlpatterns = [
    
    path('activos/', ActivosListView.as_view(), name='activos-list'),
    path('inactivos/', InactivosListView.as_view(), name='inactivos-list'),
    path('publicador/<str:estado>/', Publicador_list.as_view(), name='publicador'),
    path('irregulares/', Irregulares.as_view(), name='irregulares-list'),
    path('tarjeta/<int:pk>/', Tarjeta.as_view(), name='tarjeta'),
    path('tarjeta_inactivo/<int:pk>/', Tarjeta_Inactivo.as_view(), name='tarjeta_inactivo'),
]
