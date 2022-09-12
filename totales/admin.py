from django.contrib import admin

from .models import Publicadores, Auxiliares, Regulares

admin.site.register(Publicadores)
admin.site.register(Auxiliares)
admin.site.register(Regulares)
