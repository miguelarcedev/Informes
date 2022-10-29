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


class Publicador_list(View):
    def get(self,request,estado):
        if estado == "activo":
            publicador = Publicador.objects.filter(estado="Activo")
            cantidad = Publicador.objects.filter(estado="Activo").count()
            titulo = "PUBLICADORES ACTIVOS: "
        else:
            publicador = Publicador.objects.filter(estado="Inactivo")
            cantidad = Publicador.objects.filter(estado="Inactivo").count()
            titulo = "PUBLICADORES INACTVOS: "
        
        return render(request, "publicador/publicador.html",{"publicador": publicador, "titulo":titulo,"cantidad":cantidad})


class Irregulares(View):
    def get(self,request):
        bandera = True
        cantidad = 0
        key = []
        irregulares = []
        publicador = Publicador.objects.filter(estado="Activo").order_by('id')
        for p in publicador:
            key.append(p.id)
        informe = Informe.objects.filter(publicador=9999)
            
        for k in key:
            informe = Informe.objects.filter(publicador=k).order_by('-id')[0:6]
            bandera = True
            for i in informe:
                if i.horas == 0:
                    irregulares.append((i.publicador,i.año,i.mes))
                    if bandera:
                        cantidad += 1
                        bandera = False
            
        return render(request, "publicador/lista_irregulares.html",{"irregulares": irregulares,"cantidad":cantidad})   

           
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
