from django.contrib import admin
from django.urls import path
from . import views

from publicador.views import TarjetaPdf, ActivosListView, lista_años



urlpatterns = [
    
    path('activos/', ActivosListView.as_view(), name='activos-list'),
    path('activos_años/<int:pk>/',views.lista_años, name='activos_años_list'),
    path('tarjeta/<int:pk>/<int:año>/', TarjetaPdf.as_view(), name='tarjeta_pdf'),
    
]
