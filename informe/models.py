from email.policy import default
from django.db import models
from publicador.models import Publicador
from informes.choices import *


class Informe(models.Model):
    publicador=models.ForeignKey(Publicador, on_delete=models.CASCADE)
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    publicaciones = models.IntegerField(null=True, blank=True,default=0)
    videos = models.IntegerField(null=True, blank=True,default=0)
    horas = models.IntegerField(null=True, blank=True,default=0)
    revisitas = models.IntegerField(null=True, blank=True,default=0)
    estudios = models.IntegerField(null=True, blank=True,default=0)
    notas = models.CharField(max_length=20, choices=NOTAS, blank=True, null=True)    

    class Meta():
        verbose_name='informe'
        verbose_name_plural='informes'
        ordering=['id']

    def __str__(self):
        return str(self.publicador)
        

  
