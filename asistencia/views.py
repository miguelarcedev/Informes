from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from asistencia.models import *
from django.views.generic import  View
from django.utils import timezone
from django.db.models import Sum

# Create your views here.



def Entre_Semana_list(request, año):
    años=Entre_Semana.objects.filter(año=año)
    return render(request, "asistencia/lista_por_año.html",{"años": años, "anio":año, "entre":"entre"})

def Fin_de_Semana_list(request, año):
    años=Fin_De_Semana.objects.filter(año=año)
    return render(request, "asistencia/lista_por_año.html",{"años": años, "anio":año, "fin":"fin"})


def Entre_Semana_años(request):
    años=Entre_Semana.objects.values('año').order_by('año').annotate(suma=Sum('cantidad'))
    return render(request, "asistencia/lista_años.html",{"años": años, "entre":"entre"})

def Fin_de_Semana_años(request):
    años=Fin_De_Semana.objects.values('año').order_by('año').annotate(suma=Sum('cantidad'))
    return render(request, "asistencia/lista_años.html",{"años": años, "fin":"fin"})

class EntreSemanaPdf(View):

    def get(self, request,año, *args, **kwargs):
        
        
        template = get_template('asistencia/pdf.html')
        context = {'asistencia': Entre_Semana.objects.filter(año=año),'anio':año, 'titulo': "Reunion de entre semana"}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
       
        return response
        
class FinDeSemanaPdf(View):

    def get(self, request,año,*args, **kwargs):
        
        
        template = get_template('asistencia/pdf.html')
        context = {'asistencia': Fin_De_Semana.objects.filter(año=año),'anio':año, 'titulo': "Reunion del fin de semana"}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response