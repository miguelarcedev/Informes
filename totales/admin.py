from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Publicadores, Auxiliares, Regulares


class Pub_Resource(resources.ModelResource):

    class Meta:
        model = Publicadores

class Pub_Admin(ImportExportModelAdmin):
    resource_class = Pub_Resource
    list_display = ('año', 'mes','publicaciones','videos','horas','revisitas','estudios','informan')
    list_filter = ['año']

class Aux_Resource(resources.ModelResource):

    class Meta:
        model = Auxiliares

class Aux_Admin(ImportExportModelAdmin):
    resource_class = Aux_Resource
    list_display = ('año', 'mes','publicaciones','videos','horas','revisitas','estudios','informan')
    list_filter = ['año']

class Reg_Resource(resources.ModelResource):

    class Meta:
        model = Regulares

class Reg_Admin(ImportExportModelAdmin):
    resource_class = Reg_Resource
    list_display = ('año', 'mes','publicaciones','videos','horas','revisitas','estudios','informan')
    list_filter = ['año']

admin.site.register(Publicadores, Pub_Admin)
admin.site.register(Auxiliares, Aux_Admin)
admin.site.register(Regulares, Reg_Admin)
