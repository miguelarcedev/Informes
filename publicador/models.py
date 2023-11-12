
from django.db import models
from informes.choices import *


class Publicador(models.Model):
    apellido = models.CharField(max_length=50,null=True, blank=True)
    nombre = models.CharField(max_length=50)
    nacimiento = models.DateField(null=True, blank=True) 
    bautismo = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO)
    u_oo = models.CharField(max_length=15, choices=UOO, default='Otras Ovejas')
    a_sm = models.CharField(max_length=20, choices=ASM, null=True, blank=True)
    servicio = models.CharField(max_length=20, choices=SERVICIO, null=True, blank=True)
    grupo = models.CharField(max_length=1, choices=GRUPO)
    estado = models.CharField(max_length=10, choices=ESTADO)
    telefono = models.CharField(max_length=12, default=388)
    contacto = models.CharField(max_length=50, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=12, default=388)

    class Meta():
        verbose_name='publicador'
        verbose_name_plural='publicadores'
        ordering=['apellido']

    def __str__(self):
         return f'{self.apellido} {self.nombre}'
