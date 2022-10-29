from django.contrib import admin
from django.urls import path
from . import views

from publicador.views import Tarjeta, Tarjeta_Inactivo,Irregulares,Publicador_list



urlpatterns = [
    
    path('publicador/<str:estado>/', Publicador_list.as_view(), name='publicador'),
    path('irregulares/', Irregulares.as_view(), name='irregulares-list'),
    path('tarjeta/<int:pk>/', Tarjeta.as_view(), name='tarjeta'),
    path('tarjeta_inactivo/<int:pk>/', Tarjeta_Inactivo.as_view(), name='tarjeta_inactivo'),
]
