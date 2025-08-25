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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

    
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

""" class Precursores(LoginRequiredMixin,View):

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
        return response """
   
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
    

# Diccionario de meses de servicio
MESES_SERVICIO = {
    1: "Septiembre", 2: "Octubre", 3: "Noviembre", 4: "Diciembre",
    5: "Enero", 6: "Febrero", 7: "Marzo", 8: "Abril",
    9: "Mayo", 10: "Junio", 11: "Julio", 12: "Agosto"
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



def informe_pdf(request, año,titulo):
    # === 1) AGRUPAR POR AÑO Y MES CON TOTALES ===
    # Segun el titulo modificamos el queryset 
    if titulo == "Totales Publicadores":
        queryset = Informe.objects.filter(
            año=año,
            participacion="Si",
            auxiliar__exact = " ",  # <-- cambia según el tipo de publicador que quieras
            publicador__servicio__isnull=True,
            publicador__estado="Activo"
        ).values("año", "mes").annotate(
            total_estudios=Sum("estudios"),
            total_horas=Sum("horas"),
            total_publicadores=Count("publicador", distinct=True)
        ).order_by("mes")
    if titulo == "Totales Auxiliares":
        queryset = Informe.objects.filter(
            año=año,
            participacion="Si",
            auxiliar="Si",  # <-- cambia según el tipo de publicador que quieras
            publicador__servicio__isnull=True,
            publicador__estado="Activo"
        ).values("año", "mes").annotate(
            total_estudios=Sum("estudios"),
            total_horas=Sum("horas"),
            total_publicadores=Count("publicador", distinct=True)
        ).order_by("mes")
    if titulo == "Totales Regulares":
        queryset = Informe.objects.filter(
            año=año,
            participacion="Si",
            publicador__servicio = "Precursor Regular",
            publicador__estado="Activo"
        ).values("año", "mes").annotate(
            total_estudios=Sum("estudios"),
            total_horas=Sum("horas"),
            total_publicadores=Count("publicador", distinct=True)
        ).order_by("mes")

    # Agrupar en dict por año (aunque pedimos solo uno, mantenemos la lógica)
    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)

    # === 2) ARMAR EL PDF ===
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{titulo} {año}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Título principal
    elements.append(Paragraph(f"{titulo} - Año {año}", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Por cada año (aunque es uno en este caso)
    for año, registros in datos_por_año.items():
        # Subtítulo
        # elements.append(Paragraph(f"Año de Servicio {año}", styles["Heading2"]))
        # elements.append(Spacer(1, 8))

        # Encabezado de la tabla
        data = [["Mes", "Total Estudios", "Total Horas", "Publicadores"]]

        # Filas por cada mes
        for reg in registros:
            data.append([
                reg["mes_nombre"],
                reg["total_estudios"] or 0,
                reg["total_horas"] or 0,
                reg["total_publicadores"] or 0,
            ])

        # Crear tabla
        table = Table(data, hAlign="CENTER")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.black),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))  # espacio después de cada año

    doc.build(elements)
    return response


from django.http import HttpResponse
from django.views import View
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from .models import Publicador, Informe


class Precursores(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
        except:
            año1 = 1
            año2 = 2

        # Filtramos publicadores activos y en servicio
        publicadores = Publicador.objects.filter(servicio="Precursor Regular", estado="Activo")

        # Configuración PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="precursores.pdf"'
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # --- 2. Estilo modificado Título ---
        titulo_modificado = styles["Title"].clone('TituloModificado')
        titulo_modificado.fontName = "Helvetica-Bold"
        titulo_modificado.fontSize = 12

        # --- 2. Estilo modificado Normal  ---
        normal_modificado = styles["Normal"].clone('NormalModificado')
        normal_modificado.fontName = "Helvetica-Bold"
        normal_modificado.fontSize = 10
        normal_modificado.leading = 16

        # --- 2. Estilo modificado Normal izquierda ---
        normal_modificado_izq = styles["Normal"].clone('NormalModificado')
        normal_modificado_izq.fontName = "Helvetica"
        normal_modificado_izq.fontSize = 8
        normal_modificado_izq.leading = 12

        # Meses en el orden del año de servicio (1=Sept, ..., 12=Agosto)
        meses = [
            "Septiembre", "Octubre", "Noviembre", "Diciembre",
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto"
        ]

        for pub in publicadores:
            # Título con el nombre del publicador
            story.append(Paragraph(f"REGISTRO DE PUBLICADOR DE LA CONGREGACION", titulo_modificado))
            story.append(Paragraph(f"Nombre: {pub.apellido}, {pub.nombre}", normal_modificado))
            story.append(Paragraph(f"Fecha nacimiento: {pub.nacimiento}", normal_modificado_izq))
            story.append(Paragraph(f"Fecha bautismo: {pub.bautismo}", normal_modificado_izq))
            story.append(Paragraph(f"Sexo: {pub.sexo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.u_oo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.servicio}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.a_sm}", normal_modificado_izq))
            story.append(Spacer(1, 12))


            # ====================
            # Función auxiliar para armar tabla de un año
            def build_table(año_actual):
                data = [[año_actual, "Participación", "Estudios", "Auxiliar", "Horas", "Notas"]]

                # Total anual solo de horas
                total_horas = 0

                for mes_num, mes_nombre in enumerate(meses, start=1):
                    informe = Informe.objects.filter(
                        publicador=pub,
                        año=año_actual,
                        mes=mes_num
                    ).first()

                    if informe:
                        participacion = informe.participacion or 0
                        estudios = informe.estudios or 0
                        auxiliar = informe.auxiliar or 0
                        horas = informe.horas or 0
                        notas = informe.notas or ""
                    else:
                        participacion = estudios = auxiliar = horas = 0
                        notas = ""

                    # Acumular solo horas
                    total_horas += horas

                    data.append([mes_nombre, participacion, estudios, auxiliar, horas, notas])

                # Fila de total solo en horas
                data.append(["Total", "", "", "", total_horas, ""])

                table = Table(data, colWidths=[90, 70, 50, 50, 50, 160])
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]))
                return table

            # ====================
            # Tabla Año 1
            story.append(build_table(año1))
            story.append(Spacer(1, 20))

            # Tabla Año 2
            story.append(build_table(año2))

            # Nueva página por cada publicador
            story.append(PageBreak())

        # Generamos el PDF
        doc.build(story)
        return response

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from .models import Publicador, Informe


class Inactivos_tarjetas(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Filtramos publicadores inactivos
        publicadores = Publicador.objects.filter(estado="Inactivo")

        # Configuración PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="inactivos.pdf"'
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # --- 2. Estilo modificado Título ---
        titulo_modificado = styles["Title"].clone('TituloModificado')
        titulo_modificado.fontName = "Helvetica-Bold"
        titulo_modificado.fontSize = 12

        # --- 2. Estilo modificado Normal  ---
        normal_modificado = styles["Normal"].clone('NormalModificado')
        normal_modificado.fontName = "Helvetica-Bold"
        normal_modificado.fontSize = 10
        normal_modificado.leading = 16

        # --- 2. Estilo modificado Normal izquierda ---
        normal_modificado_izq = styles["Normal"].clone('NormalModificado')
        normal_modificado_izq.fontName = "Helvetica"
        normal_modificado_izq.fontSize = 8
        normal_modificado_izq.leading = 12


        # Meses en el orden del año de servicio (1=Septiembre ... 12=Agosto)
        meses = [
            "Septiembre", "Octubre", "Noviembre", "Diciembre",
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto"
        ]

        for pub in publicadores:
            # Buscamos el último año en el que tiene informes
            ultimo_informe = Informe.objects.filter(publicador=pub).order_by("-año").first()
            if not ultimo_informe:
                continue  # si no tiene informes, lo omitimos

            año_actual = ultimo_informe.año

            # Título con el nombre del publicador
            story.append(Paragraph(f"REGISTRO DE PUBLICADOR DE LA CONGREGACION", titulo_modificado))
            story.append(Paragraph(f"Nombre: {pub.apellido}, {pub.nombre}", normal_modificado))
            story.append(Paragraph(f"Fecha nacimiento: {pub.nacimiento}", normal_modificado_izq))
            story.append(Paragraph(f"Fecha bautismo: {pub.bautismo}", normal_modificado_izq))
            story.append(Paragraph(f"Sexo: {pub.sexo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.u_oo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.servicio}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.a_sm}", normal_modificado_izq))
            story.append(Spacer(1, 12))

            # Tabla de informes del último año activo
            data = [[año_actual, "Participación", "Estudios", "Auxiliar", "Horas", "Notas"]]

            for mes_num, mes_nombre in enumerate(meses, start=1):
                informe = Informe.objects.filter(
                    publicador=pub,
                    año=año_actual,
                    mes=mes_num
                ).first()

                if informe:
                    participacion = informe.participacion or 0
                    estudios = informe.estudios or 0
                    auxiliar = informe.auxiliar or 0
                    horas = informe.horas or 0
                    notas = informe.notas or ""
                else:
                    participacion = estudios = auxiliar = horas = 0
                    notas = ""

                data.append([mes_nombre, participacion, estudios, auxiliar, horas, notas])

            table = Table(data, colWidths=[90, 70, 50, 50, 50, 160])

            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            story.append(table)

            # Nueva página por cada publicador inactivo
            story.append(PageBreak())

        # Generamos el PDF
        doc.build(story)
        return response
