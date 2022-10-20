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
from django.db.models import  Avg

# Create your views here.


class Tarjeta(View):

    def get(self, request,pub_aux_reg, *args, **kwargs):
        if pub_aux_reg == "pub":
            ultimo_registro = Publicadores.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            promedio1 = Publicadores.objects.filter(año=año1).aggregate(Avg('horas'))
            promedio2 = Publicadores.objects.filter(año=año2).aggregate(Avg('horas'))
            context = {'totales': Publicadores.objects.all(),'año1':año1,'año2':año2, 'titulo': "PUBLICADORES - TOTALES",'promedio1': promedio1,'promedio2': promedio2}
        if pub_aux_reg == "aux":
            ultimo_registro = Auxiliares.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            promedio1 = Auxiliares.objects.filter(año=año1).aggregate(Avg('horas'))
            promedio2 = Auxiliares.objects.filter(año=año2).aggregate(Avg('horas'))
            context = {'totales': Auxiliares.objects.all(),'año1':año1,'año2':año2, 'titulo': "AUXILIARES - TOTALES",'promedio1': promedio1,'promedio2': promedio2}
        if pub_aux_reg == "reg":
            ultimo_registro = Regulares.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            promedio1 = Regulares.objects.filter(año=año1).aggregate(Avg('horas'))
            promedio2 = Regulares.objects.filter(año=año2).aggregate(Avg('horas'))
            context = {'totales': Regulares.objects.all(),'año1':año1,'año2':año2, 'titulo': "REGULARES - TOTALES",'promedio1': promedio1,'promedio2': promedio2}
        template = get_template('totales/tarjeta_totales.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response