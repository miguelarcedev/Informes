from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Informe
from publicador.models import Publicador

class Informe_Resource(resources.ModelResource):

    class Meta:
        model = Informe

class Informe_Admin(ImportExportModelAdmin):
    resource_class = Informe_Resource
    list_display = ('publicador','año', 'mes','participacion','estudios','auxiliar','horas',  'notas', 'servicio')
    list_filter = ['notas', 'año','mes']
    search_fields = ['publicador__apellido', 'publicador__nombre']

    

admin.site.register(Informe, Informe_Admin)
admin.site.site_header = "Panel de Administracion"


