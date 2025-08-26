from django.contrib import admin
from django.urls import path
from informe.views import Tarjeta_grupo, Precursores, Inactivos_tarjetas
from informe import views


urlpatterns = [
    path('tarjeta_grupo/<int:grupo>/', Tarjeta_grupo.as_view(), name='tarjeta_grupo'),
    path('precursores/tarjetas/', Precursores.as_view(), name='precursores_tarjetas'),
    path("totales_publicadores/", views.totales_publicadores, name="totales_publicadores"),
    path("totales_auxiliares/", views.totales_auxiliares, name="totales_auxiliares"),
    path("totales_regulares/", views.totales_regulares, name="totales_regulares"),
    path('informes/pdf/<int:año>/<str:titulo>/', views.informe_pdf, name='informe_pdf'),
    path('inactivos/tarjetas/', Inactivos_tarjetas.as_view(), name='inactivos_tarjetas'),
    path("publicadores_sin_informe/<int:grupo>/", views.publicadores_sin_informe, name="publicadores_sin_informe"),
]
