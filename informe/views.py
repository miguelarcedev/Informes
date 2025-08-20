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
     
    return render(request, "templates/home.html" ,{"grupos":grupos})

""" class Tarjeta_grupo(LoginRequiredMixin,View):

    def get(self, request,grupo, *args, **kwargs):
        total = 0
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        template = get_template('s-21-grupos-pdf.html')
        context = {'publicador': Publicador.objects.filter(grupo=grupo).filter(estado="Activo").filter(servicio__isnull=True),
                   'año1':año1,
                   'año2':año2,
                   'total': total,
                   }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response """

class Tarjeta_grupo(LoginRequiredMixin,View):

    def get(self, request,grupo, *args, **kwargs):
        ids = []
        totales_uno = []
        totales_dos = []
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        
        publicador = Publicador.objects.filter(grupo=grupo,estado="Activo",servicio__isnull=True)
        ids = list(publicador.values_list('id', flat=True))
        for i in ids:   
            total_horas_uno = Informe.objects.filter(publicador=i, año=año1).aggregate(total=Sum('horas'))['total']
            total_horas_dos = Informe.objects.filter(publicador=i, año=año2).aggregate(total=Sum('horas'))['total']
            totales_uno.append(total_horas_uno or 0)
            totales_dos.append(total_horas_dos or 0)
        totales_dic_uno = dict(zip(ids, totales_uno))
        totales_dic_dos = dict(zip(ids, totales_dos))
        
        context = {'publicador':publicador,
                   'año1':año1,
                   'año2':año2,
                   'totales_dic_uno':totales_dic_uno,
                   'totales_dic_dos':totales_dic_dos,
                   }
        template = get_template('s-21-grupos-pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

class Precursores(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        ids = []
        totales_uno = []
        totales_dos = []
        try:
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
        except:
            año1 = 1
            año2 = 2
        publicador = Publicador.objects.filter(servicio="Precursor Regular").filter(estado="Activo")
        ids = list(publicador.values_list('id', flat=True))
        for i in ids:   
            total_horas_uno = Informe.objects.filter(publicador=i, año=año1).aggregate(total=Sum('horas'))['total']
            total_horas_dos = Informe.objects.filter(publicador=i, año=año2).aggregate(total=Sum('horas'))['total']
            totales_uno.append(total_horas_uno or 0)
            totales_dos.append(total_horas_dos or 0)
        totales_dic_uno = dict(zip(ids, totales_uno))
        totales_dic_dos = dict(zip(ids, totales_dos))
        
        context = {'publicador':publicador,
                   'año1':año1,
                   'año2':año2,
                   'totales_dic_uno':totales_dic_uno,
                   'totales_dic_dos':totales_dic_dos,
                   }
        template = get_template('s-21-grupos-pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
   
class Inactivos(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        template = get_template('s-21-inactivos-pdf.html')
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
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febrero",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febrero",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",participacion = "Si",servicio="Publicador").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'titulo': "PUBLICADORES - TOTALES",
            'año1': año1,
            'año2': año2
            }
            
        if pub_aux_reg == "aux":
            context = {
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febrero",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febrero",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",participacion = "Si",servicio="Auxiliar").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'titulo': "AUXILIARES - TOTALES",
            'año1': año1,
            'año2': año2
            }
                
        if pub_aux_reg == "reg":
            context = {
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febrero",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febrero",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",participacion = "Si",servicio="Regular").
            aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            'titulo': "REGULARES - TOTALES",
            'año1': año1,
            'año2': año2
            }
        template = get_template('totales-pdf.html')
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
                'Septiembre': Informe.objects.filter(año=año1,mes="Septiembre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Octubre': Informe.objects.filter(año=año1,mes="Octubre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Noviembre': Informe.objects.filter(año=año1,mes="Noviembre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Diciembre': Informe.objects.filter(año=año1,mes="Diciembre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Enero': Informe.objects.filter(año=año1,mes="Enero",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Febrero': Informe.objects.filter(año=año1,mes="Febrero",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Marzo': Informe.objects.filter(año=año1,mes="Marzo",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Abril': Informe.objects.filter(año=año1,mes="Abril",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Mayo': Informe.objects.filter(año=año1,mes="Mayo",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Junio': Informe.objects.filter(año=año1,mes="Junio",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Julio': Informe.objects.filter(año=año1,mes="Julio",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Agosto': Informe.objects.filter(año=año1,mes="Agosto",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
            }
            totales2 = {
                'Septiembre': Informe.objects.filter(año=año2,mes="Septiembre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Octubre': Informe.objects.filter(año=año2,mes="Octubre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Noviembre': Informe.objects.filter(año=año2,mes="Noviembre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Diciembre': Informe.objects.filter(año=año2,mes="Diciembre",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Enero': Informe.objects.filter(año=año2,mes="Enero",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Febrero': Informe.objects.filter(año=año2,mes="Febrero",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Marzo': Informe.objects.filter(año=año2,mes="Marzo",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Abril': Informe.objects.filter(año=año2,mes="Abril",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Mayo': Informe.objects.filter(año=año2,mes="Mayo",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Junio': Informe.objects.filter(año=año2,mes="Junio",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Julio': Informe.objects.filter(año=año2,mes="Julio",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
                'Agosto': Informe.objects.filter(año=año2,mes="Agosto",participacion = "Si",servicio=pub_aux_reg).
                aggregate(Sum('horas'),Sum('estudios'),Count('id')),
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
        
        return render(request, "totales.html", context=context)
    

# app informe/views.py
from django.db.models import Sum, Count
from django.shortcuts import render
from .models import Informe

MESES_SERVICIO = {
    1: "Septiembre",
    2: "Octubre",
    3: "Noviembre",
    4: "Diciembre",
    5: "Enero",
    6: "Febrero",
    7: "Marzo",
    8: "Abril",
    9: "Mayo",
    10: "Junio",
    11: "Julio",
    12: "Agosto",
}

def totales_publicadores(request):
    titulo = "Totales Publicadores"
    queryset = Informe.objects.filter(
        participacion="Si",
        auxiliar__exact=" ",
        publicador__servicio__isnull=True,
        publicador__estado="Activo"
    ).values("año", "mes").annotate(
        total_estudios=Sum("estudios"),
        total_horas=Sum("horas"),
        total_publicadores=Count("publicador", distinct=True)
    ).order_by("-año", "mes")

    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)

    return render(request, "informe/totales.html", {"datos_por_año": datos_por_año,"titulo":titulo})

def totales_auxiliares(request):
    titulo = "Totales Auxiliares"
    queryset = Informe.objects.filter(
        participacion="Si",
        auxiliar="Si",
        publicador__servicio__isnull=True,
        publicador__estado="Activo"
    ).values("año", "mes").annotate(
        total_estudios=Sum("estudios"),
        total_horas=Sum("horas"),
        total_publicadores=Count("publicador", distinct=True)
    ).order_by("-año", "mes")

    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)

    return render(request, "informe/totales.html", {"datos_por_año": datos_por_año,"titulo":titulo})

def totales_regulares(request):
    titulo = "Totales Regulares"
    queryset = Informe.objects.filter(
        participacion="Si",
        publicador__servicio="Precursor Regular",
        publicador__estado="Activo"
    ).values("año", "mes").annotate(
        total_estudios=Sum("estudios"),
        total_horas=Sum("horas"),
        total_publicadores=Count("publicador", distinct=True)
    ).order_by("-año", "mes")

    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)

    return render(request, "informe/totales.html", {"datos_por_año": datos_por_año,"titulo":titulo})
