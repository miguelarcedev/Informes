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
from django.db.models import Count, Sum, Max
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Publicador_list(LoginRequiredMixin,View):
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

class Grupos(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        cant_grupos=Publicador.objects.filter(estado="Activo").aggregate(cantidad=Max('grupo'))
        cant_grupos=int(cant_grupos['cantidad'])
        
        i = 0
        grupo1=[]
        grupo2=[]
        grupo3=[]
        grupos = []
        g1 = Publicador.objects.filter(grupo=1, estado="Activo")
        cant1 = Publicador.objects.filter(grupo=1, estado="Activo").count()
        g2 = Publicador.objects.filter(grupo=2, estado="Activo")
        cant2 = Publicador.objects.filter(grupo=2, estado="Activo").count()
        g3 = Publicador.objects.filter(grupo=3, estado="Activo")
        cant3 = Publicador.objects.filter(grupo=3, estado="Activo").count()
        maximo =max([cant1,cant2,cant3])
        
        for uno in g1:
            grupo1.append(uno.nombre)
       
        while cant1 <= maximo:
            grupo1.append("     ")
            cant1 += 1
        for dos in g2:
            grupo2.append(dos.nombre)
        
        while cant2 <= maximo:
            grupo2.append("     ")
            cant2 += 1
        for tres in g3:
            grupo3.append(tres.nombre)
        
        while cant3 <= maximo:
            grupo3.append("     ")
            cant3 += 1
        while i <= maximo:
            grupos.append((i+1,grupo1[i],grupo2[i],grupo3[i]))
            
            i += 1
        
        template = get_template('publicador/grupos.html')
        context = {'grupos': grupos}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response

class GruposPrueba(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        matriz = []
        grupos = []
        cant_x_grupo = []
        cant_grupos=Publicador.objects.filter(estado="Activo").aggregate(cantidad=Max('grupo'))
        for i in range(int(cant_grupos['cantidad'])):
            grupos.append(Publicador.objects.filter(grupo=i+1, estado="Activo"))
            cant_x_grupo.append(Publicador.objects.filter(grupo=i+1, estado="Activo").count())
        
        maximo = max(cant_x_grupo)
        for i in range(int(cant_grupos['cantidad'])):
            print(i)
            x = cant_x_grupo[i]
            print(x)
            e = 0
            while e < maximo:
                
                if e <= x:
                    matriz[i].append(grupos[i][e])
                x += 1
        
        template = get_template('publicador/grupos.html')
        context = {'grupos': grupos}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response 

class Irregulares(LoginRequiredMixin,View):
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

           
class Tarjeta(LoginRequiredMixin,View):
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
       
class Tarjeta_Inactivo(LoginRequiredMixin,View):
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
