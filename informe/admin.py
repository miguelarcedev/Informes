from django.contrib import admin

from .models import Informe

class InformeAdmin(admin.ModelAdmin):
    list_display = ('publicador','año', 'mes','publicaciones','videos','horas', 'revisitas', 'estudios_biblicos', 'notas')

admin.site.register(Informe, InformeAdmin)
