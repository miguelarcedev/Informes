from django.db import models
from publicador.models import Publicador

# Create your models here.


MES = [
        ('Enero', 'Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
        ('Diciembre', 'Diciembre'),
]

NOTAS = [
        ('Auxiliar', 'Auxiliar'),
        ('Inactivo', 'Inactivo'),
        ('Mudado', 'Mudado'),
        ('Construccion', 'Construccion'),
        ('Enfermo', 'Enfermo'),
        ('Expulsado', 'Expulsado'),
        ('Reactivado', 'Reactivado'),
        ('Asamblea', 'Asamblea'),
        ('Escuela Precursor', 'Escuela Precursor'),
        ('Inicia Regular', 'Inicia Regular'),
        ('Nuevo Publicador', 'Nuevo Publicador'),
        
]


class Informe(models.Model):
    publicador=models.ForeignKey(Publicador, on_delete=models.CASCADE)
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    publicaciones = models.IntegerField(null=True, blank=True)
    videos = models.IntegerField(null=True, blank=True)
    horas = models.IntegerField(null=True, blank=True,default=0)
    revisitas = models.IntegerField(null=True, blank=True)
    estudios_biblicos = models.IntegerField(null=True, blank=True)
    notas = models.CharField(max_length=20, choices=NOTAS,null=True, blank=True)    

    class Meta():
        verbose_name='informe'
        verbose_name_plural='informes'
        ordering=['publicador']

    def __str__(self):
        return str(self.publicador)
        

  
