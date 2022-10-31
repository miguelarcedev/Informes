from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Entre_Semana, Fin_De_Semana


class Entre_Resource(resources.ModelResource):

    class Meta:
        model = Entre_Semana

class Entre_Admin(ImportExportModelAdmin):
    resource_class = Entre_Resource
    list_display = ('año', 'mes','cantidad','total','promedio')
    list_filter = ['año']
    readonly_fields = ['promedio']

class Fin_Resource(resources.ModelResource):

    class Meta:
        model = Fin_De_Semana

class Fin_Admin(ImportExportModelAdmin):
    resource_class = Fin_Resource
    list_display = ('año', 'mes','cantidad','total','promedio')
    list_filter = ['año']
    readonly_fields = ['promedio']


admin.site.register(Entre_Semana, Entre_Admin)
admin.site.register(Fin_De_Semana, Fin_Admin)









