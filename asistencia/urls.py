from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    path('asistencia_pdf/<str:entre_fin>/', Asistencia_pdf.as_view(), name='asistencia_pdf'),
    path('asistencia/<str:entre_fin>/', Asistencia_pantalla.as_view(), name='asistencia'),
    
]
