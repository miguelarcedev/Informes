from asyncio.windows_events import NULL
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse
from django.urls import reverse_lazy
from publicador.models import Publicador
from informe.models import Informe
from django.views.generic import  View
# Create your views here.

class ActivosListView(ListView):

    model = Publicador
    template_name = 'publicador/lista_activos.html'
    paginate_by = 100  # if pagination is desired
    def get_queryset(self):
        return Publicador.objects.filter(estado="Activo")

class InactivosListView(ListView):

    model = Publicador
    template_name = 'publicador/lista_inactivos.html'
    paginate_by = 100  # if pagination is desired
    def get_queryset(self):
        return Publicador.objects.filter(estado="Inactivo")

           
class Tarjeta(View):

    def get(self, request, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        template = get_template('publicador/tarjeta_pub.html')
        context = {'publicador': Publicador.objects.get(pk=self.kwargs['pk']),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response        
       
class Tarjeta_Inactivo(View):

    def get(self, request,pk, *args, **kwargs):
        ultimo_registro = Informe.objects.filter(publicador=pk).last()
        if ultimo_registro:
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            
        else:
            año1 = 0
            año2 = 0
            
        template = get_template('publicador/tarjeta_pub.html')
        context = {'publicador': Publicador.objects.get(pk=self.kwargs['pk']),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response        
