from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    path('asistencia/<str:entre_fin>/', Tarjeta_asistencia.as_view(), name='asistencia'),
    
]
