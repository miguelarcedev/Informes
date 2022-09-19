from django.contrib import admin
from django.urls import path

from publicador.views import TarjetaPdf, PublicadorListView



urlpatterns = [
    
    path('listar', PublicadorListView.as_view(), name='publicador-list'),
    path('tarjeta/<int:pk>/', TarjetaPdf.as_view(), name='tarjeta_pdf'),
    
]
