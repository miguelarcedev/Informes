from django.contrib import admin
from django.urls import path
from informe.views import Tarjeta_grupo, Precursores, Inactivos, Totales, TotalesPdf
from informe import views


urlpatterns = [
    path('', views.home, name='home'),
    path('tarjeta_grupo/<int:grupo>/', Tarjeta_grupo.as_view(), name='tarjeta_grupo'),
    path('precursores/', Precursores.as_view(), name='precursores'),
    path('inactivos/', Inactivos.as_view(), name='inactivos'),
    path('totales/<str:pub_aux_reg>/', Totales.as_view(), name='totales'),
    path('totales_pdf/<str:pub_aux_reg>/', TotalesPdf.as_view(), name='totales_pdf'),
    path("resumen/", views.resumen_informes, name="resumen"),
]
