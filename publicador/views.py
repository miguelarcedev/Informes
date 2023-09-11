
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
from informe.utils import get_schema_name, calculo_irregulares

# Create your views here.


class Publicador_list(LoginRequiredMixin,View):
    def get(self,request,estado):
        nombre_cong = get_schema_name()
        publicador = Publicador.objects.filter(estado=estado)
        cantidad = Publicador.objects.filter(estado=estado).count()
        if estado == "Activo":
            titulo = "PUBLICADORES ACTIVOS: "
        else:        
            titulo = "PUBLICADORES INACTVOS: "
        
        return render(request, "publicador/publicador.html",{"publicador": publicador, "titulo":titulo,"cantidad":cantidad,"estado":estado,'nombre_cong':nombre_cong[0]})

class Grupos(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        matriz_1 = []
        matriz_2 = []
        matriz_3 = []
        grupos = []
        grupo_x = []
        cantidades = []
        cantidad=Publicador.objects.filter(estado="Activo").aggregate(cantidad=Max('grupo'))

        try:
            cantidad=int(cantidad['cantidad'])

            for i in range(1,cantidad+1):
                grupos.append(Publicador.objects.filter(grupo=i, estado="Activo"))
                cantidades.append(Publicador.objects.filter(grupo=i, estado="Activo").count())
            maximo = max(cantidades)
            for i in range(9):
                grupo_x.append([])
            
            for i in range(cantidad):
                for g in grupos[i]:
                    grupo_x[i].append(g.nombre)
            for i in range(cantidad):
                x = cantidades[i]
                while x <= maximo:
                    grupo_x[i].append("     ")
                    x += 1
            
            if cantidad == 2:
                x = 0
                while x <= maximo:
                    grupo_x[2].append("     ")
                    x += 1
            if cantidad == 4:
                x = 0
                while x <= maximo:
                    grupo_x[4].append("     ")
                    grupo_x[5].append("     ")
                    x += 1
            if cantidad == 5:
                x = 0
                while x <= maximo:
                    grupo_x[5].append("     ")
                    x += 1 
            if cantidad == 7:
                x = 0
                while x <= maximo:
                    grupo_x[7].append("     ")
                    grupo_x[8].append("     ")
                    x += 1
            if cantidad == 8:
                x = 0
                while x <= maximo:
                    grupo_x[8].append("     ")
                    x += 1

            i = 0
            while i <= maximo:
                matriz_1.append((i+1,grupo_x[0][i],grupo_x[1][i],grupo_x[2][i]))
                i += 1
            if cantidad > 3 and cantidad < 7:
                i = 0
                while i <= maximo:
                    matriz_2.append((i+1,grupo_x[3][i],grupo_x[4][i],grupo_x[5][i]))
                    i += 1
            if cantidad > 6:
                i = 0
                while i <= maximo:
                    matriz_3.append((i+1,grupo_x[6][i],grupo_x[7][i],grupo_x[8][i]))
                    i += 1
        except:
            cantidad = 0

        template = get_template('publicador/grupos.html')
        context = {
            'matriz_1': matriz_1,
            'matriz_2': matriz_2,
            'matriz_3': matriz_3,
            'cantidad':cantidad}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response 

class Irregulares(LoginRequiredMixin,View):
    def get(self,request):
       calculos = calculo_irregulares()
       irregulares = calculos[0]
       cantidad = calculos[1]
       return render(request, "publicador/lista_irregulares.html",{"irregulares": irregulares,"cantidad": cantidad})   

           
class Tarjeta_Activo(LoginRequiredMixin,View):
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
        año1 = 0
        año2 = 0
        if ultimo_registro:
            año2 = ultimo_registro.año
            
        template = get_template('publicador/tarjeta_pub.html')
        context = {'publicador': Publicador.objects.get(pk=self.kwargs['pk']),'año1':año1,'año2':año2}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response        


class Estadisticas(LoginRequiredMixin,View):
    def get(self,request):

        calculos = calculo_irregulares()
        irregulares = calculos[1]
        context = {
            'irregulares': irregulares,
        }
        return render(request, "publicador/lista_irregulares.html",context=context)  