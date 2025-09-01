
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import  HttpResponse
from publicador.models import Publicador
from informe.models import Informe
from django.views.generic import  View
from django.db.models import  Sum, Max, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from informe.utils import *
from django.shortcuts import render, get_object_or_404

# Para PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors



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
       return render(request, "publicador/irregulares.html",{"irregulares": irregulares,"cantidad": cantidad})   
      

    

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

        return render(request, "publicador/estadisticas.html",context=context)  
    

    
class Contactos(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        contactos = Publicador.objects.filter(estado__contains='ctivo').values()
        context = {
            'contactos': contactos,
        }
        
        return render(request, "publicador/contactos.html",context=context)  



def publicadores_activos(request):
    titulo="Publicadores Activos"
    publicadores = Publicador.objects.filter(estado="Activo").prefetch_related("informes")
    data = []
    for pub in publicadores:
        años = {}
        for inf in pub.informes.all():
            if inf.año not in años:
                años[inf.año] = {"informes": [], "total_horas": 0}
            años[inf.año]["informes"].append(inf)
            años[inf.año]["total_horas"] += inf.horas

        data.append({
            "publicador": pub,
            "años": dict(sorted(años.items(), reverse=True))  # mostrar años descendentes
        })
    return render(request, "publicador/publicadores.html", {"data": data,"titulo": titulo})


def publicadores_inactivos(request):
    titulo="Publicadores Inactivos"
    publicadores = Publicador.objects.filter(estado="Inactivo").prefetch_related("informes")
    data = []
    for pub in publicadores:
        años = {}
        for inf in pub.informes.all():
            if inf.año not in años:
                años[inf.año] = {"informes": [], "total_horas": 0}
            años[inf.año]["informes"].append(inf)
            años[inf.año]["total_horas"] += inf.horas

        data.append({
            "publicador": pub,
            "años": dict(sorted(años.items(), reverse=True))  # mostrar años descendentes
        })
    return render(request, "publicador/publicadores.html", {"data": data,"titulo": titulo})




def informe_pdf(request, pk, anio):
    publicador = get_object_or_404(Publicador, pk=pk)

    informes = Informe.objects.filter(publicador=publicador, año=anio)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{publicador}_{anio}.pdf"'

    doc = SimpleDocTemplate(
    response,
    pagesize=A4,
    leftMargin=92,   # margen izquierdo
    rightMargin=92,  # margen derecho
    topMargin=40,    # margen superior
    bottomMargin=72  # margen inferior
)
    styles = getSampleStyleSheet()
    elements = []

    # --- 2. Estilo modificado Título ---
    titulo_modificado = styles["Title"].clone('TituloModificado')
    titulo_modificado.fontName = "Helvetica-Bold"
    titulo_modificado.fontSize = 12

    # --- 2. Estilo modificado Normal  ---
    normal_modificado = styles["Normal"].clone('NormalModificado')
    normal_modificado.fontName = "Helvetica-Bold"
    normal_modificado.fontSize = 10
    normal_modificado.leading = 16

    # --- 2. Estilo modificado Normal izquierda ---
    normal_modificado_izq = styles["Normal"].clone('NormalModificado')
    normal_modificado_izq.fontName = "Helvetica"
    normal_modificado_izq.fontSize = 8
    normal_modificado_izq.leading = 12
    
    
    # --- 3. Estilo personalizado ---
    estilo_personal = ParagraphStyle(
        name="Personal",
        fontName="Times-Roman",
        fontSize=12,
        leading=16,               # interlineado
        textColor=colors.green,
        alignment=1,              # centrado
        spaceAfter=10,
        backColor=colors.whitesmoke
    )
    
    elements.append(Paragraph(f"REGISTRO DE PUBLICADOR DE LA CONGREGACION", titulo_modificado))
    elements.append(Paragraph(f"Nombre: {publicador.apellido}, {publicador.nombre}", normal_modificado))
    elements.append(Paragraph(f"Fecha nacimiento: {publicador.nacimiento}", normal_modificado_izq))
    elements.append(Paragraph(f"Fecha bautismo: {publicador.bautismo}", normal_modificado_izq))
    elements.append(Paragraph(f"Sexo: {publicador.sexo}", normal_modificado_izq))
    elements.append(Paragraph(f"{publicador.u_oo}", normal_modificado_izq))
    elements.append(Paragraph(f"{publicador.servicio or ''}", normal_modificado_izq))
    elements.append(Paragraph(f"{publicador.a_sm or ''}", normal_modificado_izq))
    elements.append(Spacer(1, 12))

    
    # Cabecera de la tabla
    data = [[f"Año: {anio}", "Participacion", "Estudios", "Auxiliar", "Horas", "Notas                                "]]

    # Agregar filas con el nombre del mes en vez del número
    for inf in informes:
        if inf.servicio == "Auxiliar":
            aux= "Si"
        else:
            aux = " "
        data.append([
            inf.get_mes_display(), inf.participacion, inf.estudios, aux, inf.horas,
            inf.notas or ""
        ])

    tabla = Table(data, hAlign="CENTER")
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
    ]))

    elements.append(tabla)
    doc.build(elements)
    return response


def exportar_contactos_pdf(request):
    # Configuración de respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contactos.pdf"'

    # Documento con márgenes mínimos
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        leftMargin=20, rightMargin=20,
        topMargin=30, bottomMargin=20
    )

    styles = getSampleStyleSheet()
    elements = []

    # Encabezado
    elements.append(Paragraph("📒 Listado de Contactos", styles["Heading3"]))
    elements.append(Spacer(1, 10))

    # Datos de la tabla
    from .models import Publicador
    contactos = Publicador.objects.filter(estado__contains="ctivo")

    data = [["Publicador", "Teléfono", "Nombre de Contacto", "Teléfono contacto"]]
    for c in contactos:
        data.append([
            f"{c.apellido} {c.nombre}",
            c.telefono,
            c.contacto,
            c.telefono_contacto
        ])

    # Crear tabla
    table = Table(data, colWidths=[200, 100, 140, 100])

    # Estilos compactos
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ])
    table.setStyle(style)

    # Agregar tabla al documento
    elements.append(table)

    # Construir documento (se divide automáticamente en varias páginas)
    doc.build(elements)

    return response
