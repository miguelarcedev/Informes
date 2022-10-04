from django.contrib import admin
from django.urls import path
from publicador.views import TarjetaPdf
from informe import views

urlpatterns = [
    path('', views.home, name="home"),
    path('pdf/<int:pk>/', TarjetaPdf.as_view(), name='informe_pdf'),
    
]
