from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    
    path('EntreSemana/<int:año>/', EntreSemanaPdf.as_view(), name='EntreSemana_pdf'),
    path('FinDeSemana/', FinDeSemanaPdf.as_view(), name='FinDeSemana_pdf'),
    path('EntreSemana_list/', EntreSemanaListView.as_view(), name='EntreSemana_list'),
    path('Entre_Semana_list/', Entre_SemanaListView.as_view(), name='Entre_Semana_list'),
    path('Entre_Semana_anio/', views.Entre_Semana_años, name='Entre_Semana_años'),
    path('Entre_Semana_por_año/<int:año>/', views.Entre_Semana_list, name='Entre_Semana_por_año'),
]
