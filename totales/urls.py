from django import views
from django.contrib import admin
from django.urls import path

from totales.views import *
from . import views



urlpatterns = [
    path('tarjeta_totales/<str:pub_aux_reg>/', Tarjeta.as_view(), name='tarjeta_totales'),
    path('totales/<str:pub_aux_reg>/', Totales.as_view(), name='totales'),
]
