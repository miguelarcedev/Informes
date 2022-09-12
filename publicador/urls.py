from django.contrib import admin
from django.urls import path

from publicador.views import InformePdf, PublicadorListView



urlpatterns = [
    
    path('listar', PublicadorListView.as_view(), name='publicador-list'),
    path('tarjeta/<int:pk>/', InformePdf.as_view(), name='tarjeta_pdf'),
    
]
