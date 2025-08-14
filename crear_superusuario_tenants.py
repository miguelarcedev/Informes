import os

# 📌 Ajusta con el nombre real de tu proyecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informes.settings")

import django
django.setup()

from django_tenants.utils import get_tenant_model, schema_context
from django.contrib.auth import get_user_model

TenantModel = get_tenant_model()
User = get_user_model()

# Datos del superusuario que quieres replicar
SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "correo.arce@gmail.com"
SUPERUSER_PASSWORD = "superadmin"

for tenant in TenantModel.objects.all():
    if tenant.schema_name == "public":
        continue  # No crear en el schema público
    with schema_context(tenant.schema_name):
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD
            )
            print(f"✅ Superusuario creado en tenant: {tenant.schema_name}")
        else:
            print(f"ℹ️ Ya existía superusuario en tenant: {tenant.schema_name}")

print("🎯 Proceso completado.")
