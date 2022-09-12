from django.db import models

from informes.choices import MES


class Publicadores(models.Model):
    
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    publicaciones = models.IntegerField(null=True, blank=True)
    videos = models.IntegerField(null=True, blank=True)
    horas = models.IntegerField(null=True, blank=True,default=0)
    revisitas = models.IntegerField(null=True, blank=True)
    estudios_biblicos = models.IntegerField(null=True, blank=True)
    informan = models.IntegerField(null=True, blank=True)

    class Meta():
        verbose_name='publicador'
        verbose_name_plural='publicadores'
        

class Auxiliares(models.Model):
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    publicaciones = models.IntegerField(null=True, blank=True)
    videos = models.IntegerField(null=True, blank=True)
    horas = models.IntegerField(null=True, blank=True,default=0)
    revisitas = models.IntegerField(null=True, blank=True)
    estudios_biblicos = models.IntegerField(null=True, blank=True)
    informan = models.IntegerField(null=True, blank=True)

    class Meta():
        verbose_name='auxiliar'
        verbose_name_plural='auxiliares'

class Regulares(models.Model):
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    publicaciones = models.IntegerField(null=True, blank=True)
    videos = models.IntegerField(null=True, blank=True)
    horas = models.IntegerField(null=True, blank=True,default=0)
    revisitas = models.IntegerField(null=True, blank=True)
    estudios_biblicos = models.IntegerField(null=True, blank=True)
    informan = models.IntegerField(null=True, blank=True)

    class Meta():
        verbose_name='reuglar'
        verbose_name_plural='regulares'

    
    