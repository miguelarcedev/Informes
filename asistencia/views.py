
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from asistencia.models import *
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Entre_Semana
from django.db.models import Avg

# Orden deseado: septiembre → agosto
ORDEN_MESES = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]

def asistencia_entre_semana_view(request):
    titulo = "Asistencia Entre semana"
    data_por_anio = {}
    registros = Entre_Semana.objects.all().order_by("-año")

    for registro in registros:
        anio = registro.año
        if anio not in data_por_anio:
            data_por_anio[anio] = {
                "meses": [],
                "promedio_final": 0,
            }
        data_por_anio[anio]["meses"].append(registro)

    # Calcular promedio y ordenar meses
    for anio, datos in data_por_anio.items():
        promedio_final = (
            Entre_Semana.objects.filter(año=anio).aggregate(avg=Avg("promedio"))["avg"]
        )
        datos["promedio_final"] = round(promedio_final, 2) if promedio_final else 0

        # Ordenar meses de septiembre a agosto
        datos["meses"].sort(key=lambda r: ORDEN_MESES.index(r.mes))

    return render(
        request,
        "asistencia/asistencia.html",
        {"data_por_anio": data_por_anio, "titulo": titulo},
    )


def asistencia_fin_semana_view(request):
    titulo = "Asistencia Fin de semana"
    data_por_anio = {}
    registros = Fin_De_Semana.objects.all().order_by("-año")

    for registro in registros:
        anio = registro.año
        if anio not in data_por_anio:
            data_por_anio[anio] = {
                "meses": [],
                "promedio_final": 0,
            }
        data_por_anio[anio]["meses"].append(registro)

    # Calcular promedio y ordenar meses

    for anio, datos in data_por_anio.items():
        promedio_final = (
            Fin_De_Semana.objects.filter(año=anio).aggregate(avg=Avg("promedio"))["avg"]
        )
        datos["promedio_final"] = round(promedio_final, 2) if promedio_final else 0
        
        # Ordenar meses de septiembre a agosto
        datos["meses"].sort(key=lambda r: ORDEN_MESES.index(r.mes))
    
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
    response['Content-Disposition'] = f'attachment; filename="{titulo}{anio}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # --- 2. Estilo modificado Título ---
    titulo_modificado = styles["Title"].clone('TituloModificado')
    titulo_modificado.fontName = "Helvetica-Bold"
    titulo_modificado.fontSize = 12

    # Título
    elements.append(Paragraph(f"{titulo} {anio}", titulo_modificado))
    elements.append(Spacer(1, 12))

    # Tabla de registros
    data = [["Mes", "Cantidad", "Total", "Promedio"]]
    for r in registros:
        data.append([r.get_mes_display(), r.cantidad, r.total, r.promedio])

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
