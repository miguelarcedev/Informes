from urllib import response
from django.shortcuts import redirect, render
from django.db.models import Sum, Count, Max
from django.views.generic import  View
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from publicador.models import Publicador
from informe.models import Informe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def home(request):

    grupos=Publicador.objects.filter(estado="Activo").values('grupo').order_by('grupo').annotate(suma=Sum('grupo'))
    return render(request, "home.html",{"grupos": grupos})

class Tarjeta_grupo(LoginRequiredMixin,View):

    def get(self, request,grupo, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        template = get_template('informe/tarjeta_grupo.html')
        context = {'publicador': Publicador.objects.filter(grupo=grupo).filter(estado="Activo").filter(regular__isnull=True),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

class Precursores(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        template = get_template('informe/tarjeta_grupo.html')
        context = {'publicador': Publicador.objects.filter(regular="Precursor Regular").filter(estado="Activo"),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
   
class Inactivos(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        template = get_template('informe/tarjeta_inactivos.html')
        context = {'publicador': Publicador.objects.filter(estado="Inactivo")}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
  

class Totales(LoginRequiredMixin,View):

    def get(self, request,pub_aux_reg, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        if pub_aux_reg == "pub":
            context = {
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febrero",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febrero",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",horas__gt = 0,servicio="Publicador").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'titulo': "PUBLICADORES - TOTALES",
            'año1': año1,
            'año2': año2
            }
            
        if pub_aux_reg == "aux":
            context = {
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febrero",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febrero",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",horas__gt = 0,servicio="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'titulo': "AUXILIARES - TOTALES",
            'año1': año1,
            'año2': año2
            }
                
        if pub_aux_reg == "reg":
            context = {
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febrero",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febrero",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",horas__gt = 0,servicio="Regular").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'titulo': "REGULARES - TOTALES",
            'año1': año1,
            'año2': año2
            }
        template = get_template('informe/totales.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response