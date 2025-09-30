""" from django.contrib import admin
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
admin.site.site_header = "Panel de Administracion" """


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
    list_display = ('publicador', 'año', 'mes', 'participacion', 'estudios', 'horas', 'notas')
    list_filter = ['servicio','notas', 'año', 'mes']
    search_fields = ['publicador__apellido', 'publicador__nombre']

######## lo que sigue se hizo para que los usuarios comunes no puedan acceder a registros de otros ##########
######## por ahora se anula ya que el control se hace por mi panel y se restringe por tipo de usuario ########
"""    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            publicador = Publicador.objects.get(user=request.user)
            return qs.filter(publicador=publicador)
        except Publicador.DoesNotExist:
            return qs.none()

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'publicador']
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields = list(readonly_fields) + ['publicador']
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "publicador" and not request.user.is_superuser:
            try:
                publicador = Publicador.objects.get(user=request.user)
                kwargs["queryset"] = Publicador.objects.filter(id=publicador.id)
            except Publicador.DoesNotExist:
                kwargs["queryset"] = Publicador.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            try:
                publicador = Publicador.objects.get(user=request.user)
                obj.publicador = publicador
            except Publicador.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.publicador.user == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False  # Usuarios normales no pueden eliminar

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.publicador.user == request.user

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return self.search_fields
        return []  # Sin barra de búsqueda para usuarios normales

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            actions = {}  # Eliminar acciones como borrar masivo
        return actions

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser 
  """ 
admin.site.register(Informe, Informe_Admin)
admin.site.site_header = "Panel de Administración"


