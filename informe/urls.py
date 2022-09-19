from django.contrib import admin
from django.urls import path
from publicador.views import TarjetaPdf

urlpatterns = [
    
    path('pdf/<int:pk>/', TarjetaPdf.as_view(), name='informe_pdf'),
    
]
