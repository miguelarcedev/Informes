from django.contrib import admin
from django.urls import path
from . import views

from publicador.views import Tarjeta,Irregulares,Publicador_list, Grupos, Estadisticas, Publicado, Telefonos,Contactos



urlpatterns = [
    path('grupos/', Grupos.as_view(), name='grupos'),
    #path('publicadores/<str:estado>/', Publicador_list.as_view(), name='publicadores'),
    path('irregulares/', Irregulares.as_view(), name='irregulares-list'),
    path('tarjeta/<int:pk>/', Tarjeta.as_view(), name='tarjeta'),
    path('estadisticas/', Estadisticas.as_view(), name='estadisticas'),
    path('publicador/<int:pk>/', Publicado.as_view(), name='publicador'),
    path('telefonos/', Telefonos.as_view(), name='telefonos'),
    path('contactos/', Contactos.as_view(), name='contactos'),
    path("activos/", views.publicadores_activos, name="activos"),
    path("inactivos/", views.publicadores_inactivos, name="inactivos"),
    path("publicador/<int:pk>/pdf/<int:anio>/", views.informe_pdf, name="informe_pdf"),

]
