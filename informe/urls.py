from django.contrib import admin
from django.urls import path
from publicador.views import InformePdf

urlpatterns = [
    
    path('pdf/<int:pk>/', InformePdf.as_view(), name='informe_pdf'),
    
]
