from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from shared.models import Congregacion

@admin.register(Congregacion)
class CongregacionAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('nombre', 'paid_until')