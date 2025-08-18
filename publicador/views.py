
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
from asistencia.models import Entre_Semana, Fin_De_Semana
from informe.models import Informe
from django.views.generic import  View
from django.db.models import Count, Sum, Max, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from informe.utils import *

# Create your views here.


class Publicador_list(LoginRequiredMixin,View):
    def get(self,request,estado):
        publicador = Publicador.objects.filter(estado=estado)
        cantidad = Publicador.objects.filter(estado=estado).count()
        if estado == "Activo":
            titulo = "Publicadores Activos: "
        else:        
            titulo = "Publicadores Inactivos: "
        
        return render(request, "publicadores.html",{"publicador": publicador, "titulo":titulo,"cantidad":cantidad})

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
                    grupo_x[i].append(g.apellido +" "+ g.nombre)
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

        template = get_template('grupos.html')
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
       return render(request, "irregulares.html",{"irregulares": irregulares,"cantidad": cantidad})   
      

class Tarjeta(LoginRequiredMixin,View):
    def get(self, request,pk, *args, **kwargs):
        año1 = 0
        año2 = 0
        total_horas1 = 0
        total_horas2 = 0
        publicador = Publicador.objects.get(pk=self.kwargs['pk'])
        estado = publicador.estado
        if estado == "Activo":

            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            total_horas1 = Informe.objects.filter(publicador=pk, año=año1).aggregate(Sum('horas'))
            total_horas2 = Informe.objects.filter(publicador=pk, año=año2).aggregate(Sum('horas'))
            template = get_template('s-21-pdf.html')
    
        else:
            ultimo_registro = Informe.objects.filter(publicador=pk).last()
            template = get_template('s-21-inactivos-pdf.html')
            
            if ultimo_registro:
                año1 = ultimo_registro.año
            total_horas1 = Informe.objects.filter(publicador=publicador.id, año=año1).aggregate(Sum('horas'))
        publicador = Publicador.objects.filter(pk=self.kwargs['pk'])
       
        context = {'publicador': publicador ,'año1':año1,'año2':año2,'total_horas1':total_horas1,'total_horas2':total_horas2,'estado':estado}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response 
    
class Publicado(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        informe1 = {}
        informe2 = {}
        año1 = 0
        año2 = 0
        total_horas1 = 0
        total_horas2 = 0
        publicador = Publicador.objects.get(pk=self.kwargs['pk'])
        estado = publicador.estado
        if estado == "Activo":
        
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
            informe1 = Informe.objects.filter(publicador=publicador.id, año=año1)
            informe2 = Informe.objects.filter(publicador=publicador.id, año=año2)
            total_horas1 = Informe.objects.filter(publicador=publicador.id, año=año1).aggregate(Sum('horas'))
            total_horas2 = Informe.objects.filter(publicador=publicador.id, año=año2).aggregate(Sum('horas'))
        else:
            try:
                ultimo_registro = Informe.objects.filter(publicador=self.kwargs['pk']).last()
                año1 = ultimo_registro.año   
                informe1 = Informe.objects.filter(publicador=publicador.id, año=año1)
                total_horas1 = Informe.objects.filter(publicador=publicador.id, año=año1).aggregate(Sum('horas'))
            except:
                pass
        
        context = {
            'informe1': informe1,
            'informe2': informe2,
            'año1':año1,
            'año2':año2,
            'nombre': publicador.nombre,
            'apellido': publicador.apellido,
            'estado' : estado,
            'total_horas1':total_horas1,
            'total_horas2':total_horas2,
         }
       
        return render(request, "s-21.html",context=context) 

class Estadisticas(LoginRequiredMixin,View):
    def get(self,request):
        tot_activos = Publicador.objects.filter(estado="Activo").count()
        tot_inactivos = Publicador.objects.filter(estado="Inactivo").count()
        tot_no_bautizados = Publicador.objects.filter(estado="Activo", bautismo__isnull=True).count()
        tot_bautizados = tot_activos - tot_no_bautizados
        tot_hombres = Publicador.objects.filter(estado="Activo", sexo="Hombre").count()   
        tot_mujeres = tot_activos - tot_hombres
        tot_ancianos = Publicador.objects.filter(estado="Activo", a_sm="Anciano").count()
        tot_ministeriales = Publicador.objects.filter(estado="Activo", a_sm="Siervo Ministerial").count()
        tot_regulares = Publicador.objects.filter(estado="Activo", servicio="Precursor Regular").count()
        tot_ungidos = Publicador.objects.filter(estado="Activo", u_oo="Ungido").count()
        tot_otras_ovejas = tot_activos - tot_ungidos
        irregulares = calculo_irregulares()
        inactivos = calculo_inactivos()
        notas = "Nuevo Publicador"
        nuevos_publicadores = nuevo(notas)
        notas = "Bautismo"
        nuevos_bautizados = nuevo(notas)
        notas = "Reactivado"
        reactivados = nuevo(notas)
        notas = "Readmitido"
        readminitidos = nuevo(notas)   
        context = {
            'inactivos': inactivos,
            'irregulares': irregulares[1],
            'nuevos_publicadores': nuevos_publicadores,
            'nuevos_bautizados': nuevos_bautizados,
            'reactivados': reactivados,
            'readminitidos': readminitidos,
            'tot_inactivos': tot_inactivos,
            'tot_activos': tot_activos,
            'tot_inactivos': tot_inactivos,
            'tot_bautizados': tot_bautizados,
            'tot_no_bautizados': tot_no_bautizados,
            'tot_hombres': tot_hombres,
            'tot_mujeres': tot_mujeres,
            'tot_ancianos': tot_ancianos,
            'tot_ministeriales': tot_ministeriales,
            'tot_regulares': tot_regulares,
            'tot_ungidos': tot_ungidos,
            'tot_otras_ovejas': tot_otras_ovejas,
        }

        return render(request, "estadisticas.html",context=context)  
    


class S10(LoginRequiredMixin,View):
    def get(self,request):

        try:
                ultimo_registro = Informe.objects.all().last()
                año = ultimo_registro.año
                prom_entre = Entre_Semana.objects.filter(año=año).aggregate(Avg('promedio'))
                prom_fin = Fin_De_Semana.objects.filter(año=año).aggregate(Avg('promedio'))
                tot_activos = Publicador.objects.filter(estado="Activo").count()
                tot_inactivos = Informe.objects.filter(año=año, notas="Inactivo").count()
                tot_reactivados = Informe.objects.filter(año=año, notas="Reactivado").count()
                tot_sordos = 0
                tot_ciegos = 0
                context = {
                    'prom_entre': prom_entre,
                    'prom_fin': prom_fin,
                    'tot_activos': tot_activos,
                    'tot_inactivos': tot_inactivos,
                    'tot_reactivados': tot_reactivados,
                    'tot_sordos': tot_sordos,
                    'tot_ciegos': tot_ciegos,
                    'año': año,
                    }
        except:
                context = {}

        return render(request, "s-10.html",context=context)
    
class Telefonos(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        
        telefonos = Publicador.objects.filter(estado="Activo")
        context = {
            'telefonos': telefonos,
         }
       
        return render(request, "telefonos.html",context=context)
    
class Contactos(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        contactos = Publicador.objects.filter(estado__contains='ctivo').values()
        context = {
            'contactos': contactos,
        }
        
       
        return render(request, "contactos.html",context=context)      