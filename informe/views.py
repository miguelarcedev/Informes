from urllib import response
from django.shortcuts import render
from django.db.models import Sum, Count, Max
from django.views.generic import  View
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from publicador.models import Publicador
from informe.models import Informe

# Create your views here.

def home(request):

    grupos=Publicador.objects.filter(estado="Activo").values('grupo').order_by('grupo').annotate(suma=Sum('grupo'))
    return render(request, "home.html",{"grupos": grupos})

class Tarjeta_grupo(View):

    def get(self, request,grupo, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        template = get_template('informe/tarjeta_grupo.html')
        context = {'publicador': Publicador.objects.filter(grupo=grupo).filter(estado="Activo").filter(regular__isnull=True),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

class Precursores(View):

    def get(self, request, *args, **kwargs):
        ultimo_registro = Informe.objects.all().last()
        año1 = ultimo_registro.año - 1
        año2 = ultimo_registro.año
        template = get_template('informe/tarjeta_grupo.html')
        context = {'publicador': Publicador.objects.filter(regular="Precursor Regular").filter(estado="Activo"),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
   
class Inactivos(View):

    def get(self, request, *args, **kwargs):
        template = get_template('informe/tarjeta_inactivos.html')
        context = {'publicador': Publicador.objects.filter(estado="Inactivo")}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
  

