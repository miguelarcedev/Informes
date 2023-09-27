from django.contrib import admin
from django.urls import path

from publicador.views import Tarjeta_Activo, Tarjeta_Inactivo,Irregulares,Publicador_list, Grupos, Estadisticas, PublicadorActivo,PublicadorInactivo, S10, Telefonos, TelefonosContactos



urlpatterns = [
    path('grupos/', Grupos.as_view(), name='grupos'),
    path('publicador/<str:estado>/', Publicador_list.as_view(), name='publicador'),
    path('irregulares/', Irregulares.as_view(), name='irregulares-list'),
    path('tarjeta_activo/<int:pk>/', Tarjeta_Activo.as_view(), name='tarjeta_activo'),
    path('tarjeta_inactivo/<int:pk>/', Tarjeta_Inactivo.as_view(), name='tarjeta_inactivo'),
    path('estadisticas/', Estadisticas.as_view(), name='estadisticas'),
    path('publicador_activo/<int:pk>/', PublicadorActivo.as_view(), name='publicador_activo'),
    path('publicador_inactivo/<int:pk>/', PublicadorInactivo.as_view(), name='publicador_inactivo'),
    path('S10/', S10.as_view(), name='S10'),
    path('telefonos/', Telefonos.as_view(), name='telefonos'),
    path('telefonos_contactos/', TelefonosContactos.as_view(), name='telefonos_contactos'),
]
