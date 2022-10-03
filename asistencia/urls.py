from django.contrib import admin
from django.urls import path

from asistencia.views import *



urlpatterns = [
    
    
    path('EntreSemana/', EntreSemanaPdf.as_view(), name='EntreSemana_pdf'),
    path('FinDeSemana/', FinDeSemanaPdf.as_view(), name='FinDeSemana_pdf'),
    path('EntreSemana_list/', EntreSemanaListView.as_view(), name='EntreSemana_list'),
    path('Entre_Semana_list/', Entre_SemanaListView.as_view(), name='Entre_Semana_list'),
    path('Entre_Semana_anio/', Entre_Semana_añosListView.as_view(), name='Entre_Semana_años'),
]
