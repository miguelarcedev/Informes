from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    path('entre_semana/', asistencia_entre_semana_view, name='asistencia_entre_semana'),
    path('fin_semana/', asistencia_fin_semana_view, name='asistencia_fin_semana'),
    path('pdf/<int:anio>/<str:titulo>/', asistencia_pdf, name='asistencia_pdf'),
    
    
]
