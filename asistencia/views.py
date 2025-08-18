
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.



class Asistencia_pdf(LoginRequiredMixin,View):

    def get(self, request,entre_fin, *args, **kwargs):
        if entre_fin == 'entre':
            ultimo_registro = Entre_Semana.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            promedio1 = Entre_Semana.objects.filter(año=año1).aggregate(Avg('promedio'))
            promedio2 = Entre_Semana.objects.filter(año=año2).aggregate(Avg('promedio'))
            context = {
                'asistencia1': Entre_Semana.objects.filter(año=año1),
                'asistencia2': Entre_Semana.objects.filter(año=año2),
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
        
        template = get_template('asistencia-pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
    

class Asistencia_pantalla(LoginRequiredMixin,View):

    def get(self, request,entre_fin, *args, **kwargs):
        if entre_fin == 'entre':
            try:
                ultimo_registro = Entre_Semana.objects.all().last()
                año1 = ultimo_registro.año - 1
                año2 = ultimo_registro.año
                promedio1 = Entre_Semana.objects.filter(año=año1).aggregate(Avg('promedio'))
                promedio2 = Entre_Semana.objects.filter(año=año2).aggregate(Avg('promedio'))
                context = {
                    'asistencia1': Entre_Semana.objects.filter(año=año1),
                    'asistencia2': Entre_Semana.objects.filter(año=año2),
                    'titulo': "Reunion entre semana",
                    'año1':año1,
                    'promedio1': promedio1,
                    'año2':año2,
                    'promedio2': promedio2,
                    'reunion': 'entre'  
                    }
            except:
                context = {}
            
        else:
            try:
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
                    'promedio2': promedio2,
                    'reunion': 'fin'
                    }
            except:
                context = {}
        
        return render(request, "asistencia.html",context= context)