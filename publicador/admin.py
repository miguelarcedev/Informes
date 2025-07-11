from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Publicador
from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "F Y"


class PubResource(resources.ModelResource):

    class Meta:
        model = Publicador

class PubAdmin(ImportExportModelAdmin):
    resource_class = PubResource
    list_display = ('apellido','nombre','grupo','estado','user')
    list_filter = ['estado','sexo','grupo','servicio']
    search_fields = ['apellido', 'nombre', 'user__username']


admin.site.register(Publicador, PubAdmin)
