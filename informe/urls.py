from django.contrib import admin
from django.urls import path
from informe.views import Tarjeta_grupo
from informe import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tarjeta_grupo/<int:grupo>/', Tarjeta_grupo.as_view(), name='tarjeta_grupo'),
    
]
