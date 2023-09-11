from django.contrib import admin
from django.urls import path

from publicador.views import Tarjeta_Activo, Tarjeta_Inactivo,Irregulares,Publicador_list, Grupos, Estadisticas



urlpatterns = [
    path('grupos/', Grupos.as_view(), name='grupos'),
    path('publicador/<str:estado>/', Publicador_list.as_view(), name='publicador'),
    path('irregulares/', Irregulares.as_view(), name='irregulares-list'),
    path('tarjeta_activo/<int:pk>/', Tarjeta_Activo.as_view(), name='tarjeta_activo'),
    path('tarjeta_inactivo/<int:pk>/', Tarjeta_Inactivo.as_view(), name='tarjeta_inactivo'),
    path('estadisticas/', Estadisticas.as_view(), name='estadisticas'),
]
