from django.contrib import admin
from django.urls import path

from publicador.views import Tarjeta,Irregulares,Publicador_list, Grupos, Estadisticas, Publicado, S10, Telefonos,Contactos



urlpatterns = [
    path('grupos/', Grupos.as_view(), name='grupos'),
    path('publicadores/<str:estado>/', Publicador_list.as_view(), name='publicadores'),
    path('irregulares/', Irregulares.as_view(), name='irregulares-list'),
    path('tarjeta/<int:pk>/', Tarjeta.as_view(), name='tarjeta'),
    path('estadisticas/', Estadisticas.as_view(), name='estadisticas'),
    path('publicador/<int:pk>/', Publicado.as_view(), name='publicador'),
    path('S10/', S10.as_view(), name='S10'),
    path('telefonos/', Telefonos.as_view(), name='telefonos'),
    path('contactos/', Contactos.as_view(), name='contactos'),
]
