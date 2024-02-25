from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
class Congregacion(TenantMixin):
    nombre = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    
    class Meta():
        verbose_name='congregación'
        verbose_name_plural='congregaciones'
        ordering=['nombre']

    def __str__(self):
        return self.nombre
    
class Domain(DomainMixin):
    pass
