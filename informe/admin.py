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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Ver todo
        try:
            publicador = Publicador.objects.get(user=request.user)
            return qs.filter(publicador=publicador)
        except Publicador.DoesNotExist:
            return qs.none()  # No mostrar nada si el user no está vinculado

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.publicador.user == request.user

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.publicador.user == request.user

admin.site.register(Informe, Informe_Admin)
admin.site.site_header = "Panel de Administracion"


