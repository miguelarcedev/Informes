from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse, HttpResponseRedirect
from totales.models import *
from django.views.generic import  View
from django.db.models import Sum, Avg

# Create your views here.


def lista_años(request, pub_aux_reg):
    if pub_aux_reg == "pub":
        años=Publicadores.objects.values('año').order_by('año').annotate(suma=Sum('horas'))
        return render(request, "totales/lista_años.html",{"años": años, "pub":"pub"})
    if pub_aux_reg == "aux":
        años=Auxiliares.objects.values('año').order_by('año').annotate(suma=Sum('horas'))
        return render(request, "totales/lista_años.html",{"años": años, "aux":"aux"})
    if pub_aux_reg == "reg":
        años=Regulares.objects.values('año').order_by('año').annotate(suma=Sum('horas'))
        return render(request, "totales/lista_años.html",{"años": años, "reg":"reg"})

def lista_por_año(request, año, pub_aux_reg):
    if pub_aux_reg == "pub":
        años=Publicadores.objects.filter(año=año)
        promedio = Publicadores.objects.filter(año=año).aggregate(Avg('horas'))
        return render(request, "totales/lista_por_año.html",{"años": años, "anio":año, "pub":"pub",'titulo': "Totales - Publicadores",'promedio': promedio})
    if pub_aux_reg == "aux":
        años=Auxiliares.objects.filter(año=año)
        promedio = Auxiliares.objects.filter(año=año).aggregate(Avg('horas'))
        return render(request, "totales/lista_por_año.html",{"años": años, "anio":año, "aux":"aux",'titulo': "Totales - Precursores Auxiliares",'promedio': promedio})
    if pub_aux_reg == "reg":
        años=Regulares.objects.filter(año=año)
        promedio = Regulares.objects.filter(año=año).aggregate(Avg('horas'))
        return render(request, "totales/lista_por_año.html",{"años": años, "anio":año, "reg":"reg",'titulo': "Totales - Precursores Regulares",'promedio': promedio})

class tot_pub_Pdf(View):

    def get(self, request,año, *args, **kwargs):
        template = get_template('totales/tarjeta_totales.html')
        promedio = Publicadores.objects.filter(año=año).aggregate(Avg('horas'))
        context = {'totales': Publicadores.objects.filter(año=año),'anio':año, 'titulo': "Totales - Publicadores",'promedio': promedio}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
        
class tot_aux_Pdf(View):

    def get(self, request,año, *args, **kwargs):
        template = get_template('totales/tarjeta_totales.html')
        promedio = Auxiliares.objects.filter(año=año).aggregate(Avg('horas'))
        context = {'totales': Auxiliares.objects.filter(año=año),'anio':año, 'titulo': "Totales - Precursores Auxiliares",'promedio': promedio}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

class tot_reg_Pdf(View):

    def get(self, request,año, *args, **kwargs):
        template = get_template('totales/tarjeta_totales.html')
        promedio = Regulares.objects.filter(año=año).aggregate(Avg('horas'))
        context = {'totales': Regulares.objects.filter(año=año),'anio':año, 'titulo': "Totales - Precursores Regulares",'promedio': promedio}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response