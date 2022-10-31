from django.db import models
from informes.choices import MES

class Entre_Semana(models.Model):
    
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    cantidad = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    promedio = models.IntegerField(null=True, blank=True)
          

    class Meta():
        verbose_name='entre semana'
        verbose_name_plural='entre semana'
        ordering=['id']
    
    def __str__(self):
        return str(self.año) +" - " + self.mes

    def save(self):
        self.promedio = self.total / self.cantidad
        super(Entre_Semana, self).save()

    
class Fin_De_Semana(models.Model):
    
    año = models.IntegerField()
    mes = models.CharField(max_length=10, choices=MES) 
    cantidad = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    promedio = models.IntegerField(null=True, blank=True)
          

    class Meta():
        verbose_name='fin de semana'
        verbose_name_plural='fin de semana'
        ordering=['id']

    def __str__(self):
        return str(self.año) +" - " + self.mes

    def save(self):
        self.promedio = self.total / self.cantidad
        super(Entre_Semana, self).save()