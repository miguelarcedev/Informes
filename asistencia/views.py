
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse, HttpResponseRedirect
from asistencia.models import *
from django.views.generic import  View
from django.db.models import Sum, Avg

# Create your views here.


def lista_años(request, entre_fin):
    if entre_fin == "entre":
        años=Entre_Semana.objects.values('año').order_by('año').annotate(suma=Sum('cantidad'))
        return render(request, "asistencia/lista_años.html",{"años": años, "entre":"entre"})
    else:
        años=Fin_De_Semana.objects.values('año').order_by('año').annotate(suma=Sum('cantidad'))
        return render(request, "asistencia/lista_años.html",{"años": años, "fin":"fin"})

def lista_por_año(request, año, entre_fin):
    if entre_fin == "entre":
        años=Entre_Semana.objects.filter(año=año)
        promedio = Entre_Semana.objects.filter(año=año).aggregate(Avg('promedio'))
        return render(request, "asistencia/lista_por_año.html",{"años": años, "anio":año, "entre":"entre",'titulo': "Reunion de entre semana",'promedio': promedio})
    else:
        años=Fin_De_Semana.objects.filter(año=año)
        promedio = Fin_De_Semana.objects.filter(año=año).aggregate(Avg('promedio'))
        return render(request, "asistencia/lista_por_año.html",{"años": años, "anio":año, "fin":"fin",'titulo': "Reunion del fin de semana",'promedio': promedio})


class EntreSemanaPdf(View):

    def get(self, request,año, *args, **kwargs):
        template = get_template('asistencia/tarjeta_asist.html')
        promedio = Entre_Semana.objects.filter(año=año).aggregate(Avg('promedio'))
        context = {'asistencia': Entre_Semana.objects.filter(año=año),'anio':año, 'titulo': "Reunion de entre semana",'promedio': promedio}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
        
class FinDeSemanaPdf(View):

    def get(self, request,año,*args, **kwargs):
        template = get_template('asistencia/tarjeta_asist.html')
        promedio = Fin_De_Semana.objects.filter(año=año).aggregate(Avg('promedio'))
        context = {'asistencia': Fin_De_Semana.objects.filter(año=año),'anio':año, 'titulo': "Reunion del fin de semana",'promedio': promedio}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

class Tarjeta_asistencia(View):

    def get(self, request,entre_fin, *args, **kwargs):
        if entre_fin == 'entre':
            ultimo_registro = Entre_Semana.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            promedio1 = Entre_Semana.objects.filter(año=año1).aggregate(Avg('promedio'))
            promedio2 = Entre_Semana.objects.filter(año=año2).aggregate(Avg('promedio'))

            try:
                octubre2= Entre_Semana.objects.get(año=año2, mes="Octubre")
            except:
                octubre2="  "
            
            context = {
                'septiembre1': Entre_Semana.objects.get(año=año1, mes="Septiembre"),
                'octubre1': Entre_Semana.objects.get(año=año1, mes="Octubre"),
                'noviembre1': Entre_Semana.objects.get(año=año1, mes="Noviembre"),
                'diciembre1': Entre_Semana.objects.get(año=año1, mes="Diciembre"),
                'enero1': Entre_Semana.objects.get(año=año1, mes="Enero"),
                'febrero1': Entre_Semana.objects.get(año=año1, mes="Febrero"),
                'marzo1': Entre_Semana.objects.get(año=año1, mes="Marzo"),
                'abril1': Entre_Semana.objects.get(año=año1, mes="Abril"),
                'mayo1': Entre_Semana.objects.get(año=año1, mes="Mayo"),
                'junio1': Entre_Semana.objects.get(año=año1, mes="Junio"),
                'julio1': Entre_Semana.objects.get(año=año1, mes="Julio"),
                'agosto1': Entre_Semana.objects.get(año=año1, mes="Agosto"),
                'septiembre2': Entre_Semana.objects.get(año=año2, mes="Septiembre"),
                'octubre2': octubre2,
                
                'titulo': "Reunion de entre semana",
                'año1':año1,
                'promedio1': promedio1,
                'año2':año2,
                'promedio2': promedio2
                }
        else:
            ultimo_registro = Fin_De_Semana.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            promedio1 = Fin_De_Semana.objects.filter(año=año1).aggregate(Avg('promedio'))
            promedio2 = Fin_De_Semana.objects.filter(año=año2).aggregate(Avg('promedio'))
            context = {
                'asistencia1': Fin_De_Semana.objects.filter(año=año1),
                'asistencia2': Fin_De_Semana.objects.filter(año=año2),
                'titulo': "Reunion del fin de semana",
                'año1':año1,
                'promedio1': promedio1,
                'año2':año2,
                'promedio2': promedio2
                }
        
        template = get_template('asistencia/tarjeta.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response