from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    path('Entre_Semana_años/', views.Entre_Semana_años, name='Entre_Semana_años'),
    path('Fin_de_Semana_años/', views.Fin_de_Semana_años, name='Fin_de_Semana_años'),
    path('EntreSemana/<int:año>/', EntreSemanaPdf.as_view(), name='EntreSemana_pdf'),
    path('FinDeSemana/<int:año>/', FinDeSemanaPdf.as_view(), name='FinDeSemana_pdf'),
    path('Entre_Semana_por_año/<int:año>/', views.Entre_Semana_list, name='Entre_Semana_por_año'),
    path('Fin_de_Semana_por_año/<int:año>/', views.Fin_de_Semana_list, name='Fin_de_Semana_por_año'),
]
