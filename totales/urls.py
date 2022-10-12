from django import views
from django.contrib import admin
from django.urls import path

from totales.views import *
from . import views



urlpatterns = [
    
    path('lista_años/<str:pub_aux_reg>/', views.lista_años, name='lista_años'),
    path('lista_por_año/<int:año>/<str:pub_aux_reg>/', views.lista_por_año, name='lista_por_año'),
    path('tot_pub/<int:año>/', tot_pub_Pdf.as_view(), name='tot_pub_pdf'),
    path('tot_aux/<int:año>/', tot_aux_Pdf.as_view(), name='tot_aux_pdf'),
    path('tot_reg/<int:año>/', tot_reg_Pdf.as_view(), name='tot_reg_pdf'),
]
