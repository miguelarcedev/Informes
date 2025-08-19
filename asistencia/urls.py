from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    #path('asistencia_pdf/<str:entre_fin>/', Asistencia_pdf.as_view(), name='asistencia_pdf'),
    #path('asistencia/<str:entre_fin>/', Asistencia_pantalla.as_view(), name='asistencia'),
    path('entre_semana/', asistencia_entre_semana_view, name='asistencia_entre_semana'),
    path('fin_semana/', asistencia_fin_semana_view, name='asistencia_fin_semana'),
    path('pdf/<int:anio>/<str:titulo>/', asistencia_pdf, name='asistencia_pdf'),
    
    
]
