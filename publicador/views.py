
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import  HttpResponse
from publicador.models import Publicador
from asistencia.models import Entre_Semana, Fin_De_Semana
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



# Definición de meses del año de servicio (septiembre–agosto)

MESES_SERVICIO = [
    "Septiembre", "Octubre", "Noviembre", "Diciembre",
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
]

def informe_pdf(request, pk, anio):
    publicador = get_object_or_404(Publicador, pk=pk)

    informes = Informe.objects.filter(publicador=publicador, año=anio).order_by("mes")

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
    elements.append(Paragraph(f"{publicador.servicio}", normal_modificado_izq))
    elements.append(Paragraph(f"{publicador.a_sm}", normal_modificado_izq))
    elements.append(Spacer(1, 12))

    
    # Cabecera de la tabla
    data = [[f"Año: {anio}", "Participacion", "Estudios", "Auxiliar", "Horas", "Notas                                "]]

    # Agregar filas con el nombre del mes en vez del número
    for inf in informes:
        nombre_mes = MESES_SERVICIO[inf.mes - 1]  # inf.mes = 1 → Septiembre
        data.append([
            nombre_mes, inf.participacion, inf.estudios, inf.auxiliar, inf.horas,
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
