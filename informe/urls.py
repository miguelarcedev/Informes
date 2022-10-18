from django.contrib import admin
from django.urls import path
from informe.views import Tarjeta_grupo, Precursores, Inactivos
from informe import views


urlpatterns = [
    path('', views.home, name="home"),
    path('tarjeta_grupo/<int:grupo>/', Tarjeta_grupo.as_view(), name='tarjeta_grupo'),
    path('precursores/', Precursores.as_view(), name='precursores'),
    path('inactivos/', Inactivos.as_view(), name='inactivos'),
]
