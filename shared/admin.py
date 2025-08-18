from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from shared.models import Congregacion, Domain


@admin.register(Congregacion)
class CongregacionAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('nombre', 'created_on', 'auto_create_schema')


@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('domain','is_primary', 'tenant_id')