from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
from publicador.models import Publicador
from informe.models import Informe
from django.views.generic import  View
from django.db.models import Sum, Avg



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

def lista_años(request, pk):
    
    años=Informe.objects.filter(publicador=pk).values('año').order_by('año').annotate(suma=Sum('horas'))
    return render(request, "publicador/lista_años.html",{"años": años,"pk": pk})


class TarjetaPdf(View):
    año = datetime.datetime.today().year
    mes = datetime.datetime.today().month
    año1 = 0
    año2 = 0

    if mes == "Octubre" or mes == "Noviembre" or mes == "Diciembre":
        año1 = año
        año2 = año +1
    else:
        año1 = año - 1
        año2 = año

    def get(self, request,año, *args, **kwargs):
        template = get_template('publicador/tarjeta_pub.html')
        context = {'publicador': Publicador.objects.get(pk=self.kwargs['pk']),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
      
           
        
       

