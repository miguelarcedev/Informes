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
from informe.utils import get_schema_name


# @login_required
# def home(request):
#     grupos=Publicador.objects.filter(estado="Activo").values('grupo').order_by('grupo').annotate(suma=Sum('grupo'))
#     return render(request, "home.html",{"grupos": grupos})

@login_required
def home(request):
    grupos = []
    
    cantidad=Publicador.objects.filter(estado="Activo").aggregate(cantidad=Max('grupo'))
    
    try:
        cantidad=int(cantidad['cantidad'])
    except:
        cantidad = 0
    if cantidad > 0:
        for i in range(1,cantidad+1):
            grupos.append(i)
    
    nombre = get_schema_name() # se llama a la función para obtener el nombre del esquema actual

      
    return render(request, "home.html",{"grupos":grupos,'nombre':nombre[0]})

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
        try:
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
        except:
            año1 = 1
            año2 = 2
        template = get_template('informe/tarjeta_grupo.html')
        context = {
            'publicador': Publicador.objects.filter(regular="Precursor Regular").filter(estado="Activo"),
            'año1':año1,
            'año2':año2
            }
        
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
  

class TotalesPdf(LoginRequiredMixin,View):

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
    
class Totales(LoginRequiredMixin,View):

    def get(self, request,pub_aux_reg, *args, **kwargs):
        
        if pub_aux_reg == "Publicador":
            titulo = "TOTALES PUBLICADORES"
        if pub_aux_reg == "Auxiliar":
            titulo = "TOTALES AUXILIARES"
        if pub_aux_reg == "Regular":
            titulo = "TOTALES REGULARES"    
        
        try:
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año

            totales1 = {
                'Septiembre': Informe.objects.filter(año=año1,mes="Septiembre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Octubre': Informe.objects.filter(año=año1,mes="Octubre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Noviembre': Informe.objects.filter(año=año1,mes="Noviembre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Diciembre': Informe.objects.filter(año=año1,mes="Diciembre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Enero': Informe.objects.filter(año=año1,mes="Enero",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Febrero': Informe.objects.filter(año=año1,mes="Febrero",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Marzo': Informe.objects.filter(año=año1,mes="Marzo",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Abril': Informe.objects.filter(año=año1,mes="Abril",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Mayo': Informe.objects.filter(año=año1,mes="Mayo",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Junio': Informe.objects.filter(año=año1,mes="Junio",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Julio': Informe.objects.filter(año=año1,mes="Julio",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Agosto': Informe.objects.filter(año=año1,mes="Agosto",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            }
            totales2 = {
                'Septiembre': Informe.objects.filter(año=año2,mes="Septiembre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Octubre': Informe.objects.filter(año=año2,mes="Octubre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Noviembre': Informe.objects.filter(año=año2,mes="Noviembre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Diciembre': Informe.objects.filter(año=año2,mes="Diciembre",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Enero': Informe.objects.filter(año=año2,mes="Enero",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Febrero': Informe.objects.filter(año=año2,mes="Febrero",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Marzo': Informe.objects.filter(año=año2,mes="Marzo",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Abril': Informe.objects.filter(año=año2,mes="Abril",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Mayo': Informe.objects.filter(año=año2,mes="Mayo",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Junio': Informe.objects.filter(año=año2,mes="Junio",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Julio': Informe.objects.filter(año=año2,mes="Julio",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
                'Agosto': Informe.objects.filter(año=año2,mes="Agosto",horas__gt = 0,servicio=pub_aux_reg).
                aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            }
        except:
            año1= 1
            año2= 1
            totales1= {}
            totales2= {}
            
        datos = {
            'titulo': titulo,
            'año1': año1,
            'año2': año2,
            'pub_aux_reg': pub_aux_reg,
            }
        context = {
            'totales1':totales1,
            'totales2':totales2,
            'datos':datos
        }
            
        return render(request, "informe/pantalla.html", context=context)