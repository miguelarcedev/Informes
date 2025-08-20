
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
        
        return render(request, "asistencia/asistencia.html",context= context)
    

# asistencia/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Entre_Semana
from django.db.models import Avg

def asistencia_entre_semana_view(request):
    from django.db.models import Avg
    titulo = "Asistencia Entre semana"
    data_por_anio = {}
    registros = Entre_Semana.objects.all().order_by('-año','mes')

    for registro in registros:
        anio = registro.año
        if anio not in data_por_anio:
            data_por_anio[anio] = {
                "meses": [],
                "promedio_final": 0,
            }
        data_por_anio[anio]["meses"].append(registro)

    for anio, datos in data_por_anio.items():
        promedio_final = (
            Entre_Semana.objects.filter(año=anio).aggregate(avg=Avg("promedio"))["avg"]
        )
        datos["promedio_final"] = round(promedio_final, 2) if promedio_final else 0

    return render(request, "asistencia/asistencia.html", {"data_por_anio": data_por_anio, "titulo":titulo})

def asistencia_fin_semana_view(request):
    from django.db.models import Avg
    titulo = "Asistencia Fin de semana"
    data_por_anio = {}
    registros = Fin_De_Semana.objects.all().order_by('-año','mes')

    for registro in registros:
        anio = registro.año
        if anio not in data_por_anio:
            data_por_anio[anio] = {
                "meses": [],
                "promedio_final": 0,
            }
        data_por_anio[anio]["meses"].append(registro)

    for anio, datos in data_por_anio.items():
        promedio_final = (
            Fin_De_Semana.objects.filter(año=anio).aggregate(avg=Avg("promedio"))["avg"]
        )
        datos["promedio_final"] = round(promedio_final, 2) if promedio_final else 0

    return render(request, "asistencia/asistencia.html", {"data_por_anio": data_por_anio, "titulo":titulo})


def asistencia_pdf(request, anio, titulo):
    # Filtrar registros del año seleccionado segun tabla
    if titulo == "Asistencia Entre semana":
        registros = Entre_Semana.objects.filter(año=anio)
        promedio_final = registros.aggregate(avg=Avg("promedio"))["avg"] or 0
        promedio_final = round(promedio_final, 2)
    else:
        registros = Fin_De_Semana.objects.filter(año=anio)
        promedio_final = registros.aggregate(avg=Avg("promedio"))["avg"] or 0
        promedio_final = round(promedio_final, 2)
    
    # Preparar respuesta como PDF
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="asistencia_{anio}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph(f"{titulo}", styles["Title"]))
    elements.append(Paragraph(f"Año {anio}", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Tabla de registros
    data = [["Mes", "Cantidad", "Total", "Promedio"]]
    for r in registros:
        data.append([r.mes, r.cantidad, r.total, r.promedio])

    # Agregar fila del promedio final
    data.append(["", "", "Promedio Final", promedio_final])

    table = Table(data, hAlign="CENTER")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#343a40")),  # encabezado
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#f8f9fa")),
    ]))
    elements.append(table)

    doc.build(elements)
    return response
