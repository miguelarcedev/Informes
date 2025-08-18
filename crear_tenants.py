import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informes.settings")
django.setup()

from shared.models import Congregacion, Domain

def crear_tenant(nombre, esquema, dominio):
    tenant = Congregacion(schema_name=esquema, nombre=nombre)
    tenant.save()
    Domain.objects.create(domain=dominio, tenant=tenant, is_primary=True)

if __name__ == "__main__":
    crear_tenant("Alto Comedero", "Alto_Comedero", "ac.localhost")
    crear_tenant("Plaza Hipotecario", "Plaza_Hipotecario", "ph.localhost")
    print("Tenants creados correctamente.")
