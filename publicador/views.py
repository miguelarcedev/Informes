from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from publicador.models import Publicador
from django.views.generic import  View


# Create your views here.

class PublicadorListView(ListView):

    model = Publicador
    template_name = 'publicador/lista_activos.html'
    paginate_by = 25  # if pagination is desired
    def get_queryset(self):
        return Publicador.objects.filter(estado="Activo")


class TarjetaPdf(View):

    def get(self, request, *args, **kwargs):
        
        
        template = get_template('publicador/tarjeta.html')
        context = {'publicador': Publicador.objects.get(pk=self.kwargs['pk'])}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response
      
           
        
       

