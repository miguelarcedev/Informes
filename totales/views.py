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
from django.db.models import  Avg, Sum, Count
from informe.models import Informe

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

class Totales(View):

    def get(self, request,pub_aux_reg, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        if pub_aux_reg == "pub":
            context = {'totales': Informe.objects.filter(año=año1),
                'año1':año1,'año2':año2,
                'titulo': "PUBLICADORES - TOTALES",
                'promedio1': promedio1,
                'promedio2': promedio2}
        if pub_aux_reg == "aux":
            context = {
            'septiembre1': Informe.objects.filter(año=año1,mes="Septiembre",horas__gt = 0,notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre1': Informe.objects.filter(año=año1,mes="Octubre",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre1': Informe.objects.filter(año=año1,mes="Noviembre",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre1': Informe.objects.filter(año=año1,mes="Diciembre",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero1': Informe.objects.filter(año=año1,mes="Enero",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero1': Informe.objects.filter(año=año1,mes="Febreo",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo1': Informe.objects.filter(año=año1,mes="Marzo",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril1': Informe.objects.filter(año=año1,mes="Abril",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo1': Informe.objects.filter(año=año1,mes="Mayo",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio1': Informe.objects.filter(año=año1,mes="Junio",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio1': Informe.objects.filter(año=año1,mes="Julio",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto1': Informe.objects.filter(año=año1,mes="Agosto",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'septiembre2': Informe.objects.filter(año=año2,mes="Septiembre",horas__gt = 0,notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'octubre2': Informe.objects.filter(año=año2,mes="Octubre",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'noviembre2': Informe.objects.filter(año=año2,mes="Noviembre",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'diciembre2': Informe.objects.filter(año=año2,mes="Diciembre",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'enero2': Informe.objects.filter(año=año2,mes="Enero",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'febrero2': Informe.objects.filter(año=año2,mes="Febreo",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'marzo2': Informe.objects.filter(año=año2,mes="Marzo",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'abril2': Informe.objects.filter(año=año2,mes="Abril",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'mayo2': Informe.objects.filter(año=año2,mes="Mayo",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'junio2': Informe.objects.filter(año=año2,mes="Junio",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'julio2': Informe.objects.filter(año=año2,mes="Julio",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'agosto2': Informe.objects.filter(año=año2,mes="Agosto",notas="Auxiliar").
            aggregate(Sum('publicaciones'),Sum('videos'),Sum('horas'),Sum('revisitas'),Sum('estudios'),Count('id')),
            'titulo': "AUXILIARES - TOTALES",
            'año1': año1,
            'año2': año2
            }
                
        if pub_aux_reg == "reg":
            promedio1 = Regulares.objects.filter(año=año1).aggregate(Avg('horas'))
            promedio2 = Regulares.objects.filter(año=año2).aggregate(Avg('horas'))
            context = {'totales': Regulares.objects.all(),'año1':año1,'año2':año2, 'titulo': "REGULARES - TOTALES",'promedio1': promedio1,'promedio2': promedio2}
        template = get_template('totales/totales.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response