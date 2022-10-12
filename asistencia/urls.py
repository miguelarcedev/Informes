from django import views
from django.contrib import admin
from django.urls import path

from asistencia.views import *
from . import views



urlpatterns = [
    
    path('lista_años/<str:entre_fin>/', views.lista_años, name='lista_años'),
    path('lista_por_año/<int:año>/<str:entre_fin>/', views.lista_por_año, name='lista_por_año'),
    path('EntreSemana/<int:año>/', EntreSemanaPdf.as_view(), name='EntreSemana_pdf'),
    path('FinDeSemana/<int:año>/', FinDeSemanaPdf.as_view(), name='FinDeSemana_pdf'),
    
]
