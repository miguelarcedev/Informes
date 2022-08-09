from unittest.mock import DEFAULT
from django.db import models


SEXO = [
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre'),
    ]
    
UOO = [
        ('Ungido', 'Ungido'),
        ('Otras Ovejas', 'Otras Ovejas'),
    ]

ASM = [
        ('Anciano', 'Anciano'),
        ('Siervo Ministerial', 'Siervo Ministerial'),
    ]

PR = [
        ('Precursor Regular', 'Precursor Regular'),
        
    ]

GRUPO = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        
    ]

ESTADO = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Mudado', 'Mudado'),
        ('Fallecido', 'Fallecido'),
        
    ]


class Publicador(models.Model):
    nombre = models.CharField(max_length=50)
    nacimiento = models.DateField(null=True, blank=True) 
    bautismo = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO)
    u_oo = models.CharField(max_length=15, choices=UOO, default='Otras Ovejas')
    a_sm = models.CharField(max_length=20, choices=ASM, null=True, blank=True)
    regular = models.CharField(max_length=20, choices=PR, null=True, blank=True)
    grupo = models.CharField(max_length=1, choices=GRUPO)
    estado = models.CharField(max_length=10, choices=ESTADO)
    

    class Meta():
        verbose_name='publicador'
        verbose_name_plural='publicadores'
        ordering=['nombre']

    def __str__(self):
        return self.nombre
