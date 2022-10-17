from urllib import response
from django.shortcuts import render
from django.db.models import Sum, Count, Max
from django.views.generic import  View
from django.template.loader import get_template
from django.shortcuts import render
from django.http import HttpResponse
from xhtml2pdf import pisa
from publicador.models import Publicador

# Create your views here.

def home(request):

    grupos=Publicador.objects.filter(estado="Activo").values('grupo').order_by('grupo').annotate(suma=Sum('grupo'))
    return render(request, "home.html",{"grupos": grupos})

class Tarjeta_grupo(View):

    def get(self, request,grupo, *args, **kwargs):
        template = get_template('informe/tarjeta_grupo.html')
        context = {'publicador': Publicador.objects.filter(grupo=grupo),'año':2022}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

   
  

