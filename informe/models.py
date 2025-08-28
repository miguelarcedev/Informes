from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from publicador.models import Publicador
from informes.choices import *


class Informe(models.Model):
    publicador = models.ForeignKey(Publicador, on_delete=models.CASCADE, related_name="informes")
    año = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(choices=MES) 
    participacion = models.CharField(max_length=2,choices=SINO,null=False, blank=False)
    estudios = models.IntegerField(null=True, blank=True,default=0)
    auxiliar = models.CharField(max_length=2, choices=SINO,null=True, blank=True)
    horas = models.IntegerField(null=True, blank=True,default=0)
    notas = models.CharField(max_length=40, choices=NOTAS, blank=True, null=True)
    servicio = models.CharField(max_length=10, choices=INF_SERVICIO, blank=False, null=False)

    class Meta():
        unique_together = ('publicador', 'año', 'mes')  # Un informe por mes y año por publicador
        verbose_name='informe'
        verbose_name_plural='informes'
        ordering=['id']

    def __str__(self):
        return str(self.publicador)
        

  
