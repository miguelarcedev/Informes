from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from publicador.models import Publicador
from informes.choices import *


class Informe(models.Model):
    publicador=models.ForeignKey(Publicador, on_delete=models.CASCADE)
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    participacion = models.CharField(max_length=10, choices=SINO,default=" ")
    estudios = models.IntegerField(null=True, blank=True,default=0)
    auxiliar = models.CharField(max_length=10, choices=SINO,default=" ")
    horas = models.IntegerField(null=True, blank=True,default=0)
    notas = models.CharField(max_length=40, choices=NOTAS, blank=True, null=True)
   

    class Meta():
        unique_together = ('publicador', 'año', 'mes')  # Un informe por mes y año por publicador
        verbose_name='informe'
        verbose_name_plural='informes'
        ordering=['id']

    def __str__(self):
        return str(self.publicador)
        

  
