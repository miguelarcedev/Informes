from django.contrib import admin

from .models import Publicador

class PublicadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    

admin.site.register(Publicador, PublicadorAdmin)
