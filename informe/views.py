from django.db.models import Sum, Count, Max
from django.views.generic import  View
from django.shortcuts import render
from django.http import HttpResponse
from publicador.models import Publicador
from informe.models import Informe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.views import View
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from datetime import date



# Diccionario de meses de servicio
MESES_SERVICIO = {
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    
}

# Orden deseado: septiembre → agosto
ORDEN_MESES = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]

def totales_publicadores(request):
    titulo = "Totales Publicadores"
    queryset = Informe.objects.filter(
        participacion="Si",
        servicio="Publicador",
    ).values("año", "mes").annotate(
        total_estudios=Sum("estudios"),
        total_horas=Sum("horas"),
        total_publicadores=Count("publicador", distinct=True)
    ).order_by("-año")

    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)

    # Reordenar meses por año según ORDEN_MESES
    for año in datos_por_año:
        datos_por_año[año].sort(
            key=lambda x: ORDEN_MESES.index(x["mes"])
        )

    return render(
        request,
        "informe/totales.html",
        {"datos_por_año": datos_por_año, "titulo": titulo}
    )

def totales_auxiliares(request):
    titulo = "Totales Auxiliares"
    queryset = Informe.objects.filter(
        participacion="Si",
        servicio = "Auxiliar",
    ).values("año", "mes").annotate(
        total_estudios=Sum("estudios"),
        total_horas=Sum("horas"),
        total_publicadores=Count("publicador", distinct=True)
    ).order_by("-año")

    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)

    # Reordenar meses por año según ORDEN_MESES
    for año in datos_por_año:
        datos_por_año[año].sort(
            key=lambda x: ORDEN_MESES.index(x["mes"])
        )

    return render(request, "informe/totales.html", {"datos_por_año": datos_por_año,"titulo":titulo})

def totales_regulares(request):
    titulo = "Totales Regulares"
    queryset = Informe.objects.filter(
        participacion="Si",
        servicio = "Regular",
    ).values("año", "mes").annotate(
        total_estudios=Sum("estudios"),
        total_horas=Sum("horas"),
        total_publicadores=Count("publicador", distinct=True)
    ).order_by("-año")

    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)
    
    # Reordenar meses por año según ORDEN_MESES
    for año in datos_por_año:
        datos_por_año[año].sort(
            key=lambda x: ORDEN_MESES.index(x["mes"])
        )

    return render(request, "informe/totales.html", {"datos_por_año": datos_por_año,"titulo":titulo})



def informe_pdf(request, año,titulo):
    # === 1) AGRUPAR POR AÑO Y MES CON TOTALES ===
    # Segun el titulo modificamos el queryset 
    if titulo == "Totales Publicadores":
        queryset = Informe.objects.filter(
            año=año,
            participacion="Si",
            servicio = "Publicador",  # <-- cambia según el tipo de publicador que quieras
            publicador__estado="Activo"
        ).values("año", "mes").annotate(
            total_estudios=Sum("estudios"),
            total_horas=Sum("horas"),
            total_publicadores=Count("publicador", distinct=True)
        )
    if titulo == "Totales Auxiliares":
        queryset = Informe.objects.filter(
            año=año,
            participacion="Si",
            servicio="Auxiliar",  # <-- cambia según el tipo de publicador que quieras
            publicador__estado="Activo"
        ).values("año", "mes").annotate(
            total_estudios=Sum("estudios"),
            total_horas=Sum("horas"),
            total_publicadores=Count("publicador", distinct=True)
        )
    if titulo == "Totales Regulares":
        queryset = Informe.objects.filter(
            año=año,
            participacion="Si",
            servicio = "Regular",
            publicador__estado="Activo"
        ).values("año", "mes").annotate(
            total_estudios=Sum("estudios"),
            total_horas=Sum("horas"),
            total_publicadores=Count("publicador", distinct=True)
        )

    # Agrupar en dict por año (aunque pedimos solo uno, mantenemos la lógica)
    datos_por_año = {}
    for row in queryset:
        año = row["año"]
        mes_num = row["mes"]
        row["mes_nombre"] = MESES_SERVICIO.get(mes_num, "")
        if año not in datos_por_año:
            datos_por_año[año] = []
        datos_por_año[año].append(row)
    
    # Reordenar meses por año según ORDEN_MESES
    for año in datos_por_año:
        datos_por_año[año].sort(
            key=lambda x: ORDEN_MESES.index(x["mes"])
        )

    # === 2) ARMAR EL PDF ===
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{titulo} {año}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # --- 2. Estilo modificado Título ---
    titulo_modificado = styles["Title"].clone('TituloModificado')
    titulo_modificado.fontName = "Helvetica-Bold"
    titulo_modificado.fontSize = 12
    # Título principal
    elements.append(Paragraph(f"{titulo} - Año {año}", titulo_modificado))
    elements.append(Spacer(1, 12))

    # Por cada año (aunque es uno en este caso)
    for año, registros in datos_por_año.items():
        # Subtítulo
        # elements.append(Paragraph(f"Año de Servicio {año}", styles["Heading2"]))
        # elements.append(Spacer(1, 8))

        # Encabezado de la tabla
        data = [["Mes", "Total Estudios", "Total Horas", "Publicadores"]]

        # Filas por cada mes
        for reg in registros:
            data.append([
                reg["mes_nombre"],
                reg["total_estudios"] or 0,
                reg["total_horas"] or 0,
                reg["total_publicadores"] or 0,
            ])

        # Crear tabla
        table = Table(data, hAlign="CENTER")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.black),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))  # espacio después de cada año

    doc.build(elements)
    return response



class Precursores(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
        except:
            año1 = 1
            año2 = 2

        # Filtramos publicadores activos y en servicio
        publicadores = Publicador.objects.filter(servicio="Precursor Regular", estado="Activo")

        # Configuración PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="precursores.pdf"'
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

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

        for pub in publicadores:
            # Título con el nombre del publicador
            story.append(Paragraph(f"REGISTRO DE PUBLICADOR DE LA CONGREGACION", titulo_modificado))
            story.append(Paragraph(f"Nombre: {pub.apellido}, {pub.nombre}", normal_modificado))
            story.append(Paragraph(f"Fecha nacimiento: {pub.nacimiento}", normal_modificado_izq))
            story.append(Paragraph(f"Fecha bautismo: {pub.bautismo}", normal_modificado_izq))
            story.append(Paragraph(f"Sexo: {pub.sexo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.u_oo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.servicio}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.a_sm}", normal_modificado_izq))
            story.append(Spacer(1, 12))


            # ====================
            # Función auxiliar para armar tabla de un año
            def build_table(año_actual):
                data = [[año_actual, "Participación", "Estudios", "Auxiliar", "Horas", "Notas"]]
                total_horas = 0

                # Traer registros ya ordenados según la BD
                informes = Informe.objects.filter(
                    publicador=pub,
                    año=año_actual
                ).order_by("id")   # o por el campo que asegura tu orden Sept→Ago

                for informe in informes:
                    participacion = informe.participacion or 0
                    estudios = informe.estudios or 0
                    auxiliar = informe.auxiliar or 0
                    horas = informe.horas or 0
                    notas = informe.notas or ""

                    total_horas += horas

                    # Convertir mes numérico a nombre
                    mes_nombre = MESES_SERVICIO.get(informe.mes, "")

                    data.append([mes_nombre, participacion, estudios, auxiliar, horas, notas])

                # Fila total de horas
                data.append(["Total", "", "", "", total_horas, ""])

                table = Table(data, colWidths=[90, 70, 50, 50, 50, 160])
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]))
                return table


            # ====================
            # Tabla Año 1
            story.append(build_table(año1))
            story.append(Spacer(1, 20))

            # Tabla Año 2
            story.append(build_table(año2))

            # Nueva página por cada publicador
            story.append(PageBreak())

        # Generamos el PDF
        doc.build(story)
        return response


class Inactivos_tarjetas(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Filtramos publicadores inactivos
        publicadores = Publicador.objects.filter(estado="Inactivo")

        # Configuración PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="inactivos.pdf"'
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

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

        for pub in publicadores:
            # Buscamos el último año en el que tiene informes
            ultimo_informe = Informe.objects.filter(publicador=pub).order_by("-año").first()
            if not ultimo_informe:
                continue  # si no tiene informes, lo omitimos

            año_actual = ultimo_informe.año

            # Título con el nombre del publicador
            story.append(Paragraph(f"REGISTRO DE PUBLICADOR DE LA CONGREGACION", titulo_modificado))
            story.append(Paragraph(f"Nombre: {pub.apellido}, {pub.nombre}", normal_modificado))
            story.append(Paragraph(f"Fecha nacimiento: {pub.nacimiento}", normal_modificado_izq))
            story.append(Paragraph(f"Fecha bautismo: {pub.bautismo}", normal_modificado_izq))
            story.append(Paragraph(f"Sexo: {pub.sexo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.u_oo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.servicio}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.a_sm}", normal_modificado_izq))
            story.append(Spacer(1, 12))

            # Tabla de informes del último año activo
            data = [[año_actual, "Participación", "Estudios", "Auxiliar", "Horas", "Notas"]]

            # Traer informes de ese año ya en el orden guardado en la tabla
            informes = Informe.objects.filter(
                publicador=pub,
                año=año_actual
            ).order_by("id")  # usa el campo que respeta tu orden Sept→Ago

            for informe in informes:
                participacion = informe.participacion or 0
                estudios = informe.estudios or 0
                auxiliar = informe.auxiliar or 0
                horas = informe.horas or 0
                notas = informe.notas or ""

                mes_nombre = MESES_SERVICIO.get(informe.mes, "")

                data.append([mes_nombre, participacion, estudios, auxiliar, horas, notas])

            table = Table(data, colWidths=[90, 70, 50, 50, 50, 160])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            story.append(table)

            # Nueva página por cada publicador inactivo
            story.append(PageBreak())

        # Generamos el PDF
        doc.build(story)
        return response


class Tarjeta_grupo(LoginRequiredMixin, View):

    def get(self, request,grupo, *args, **kwargs):
        try:
            ultimo_registro = Informe.objects.all().last()
            año1 = ultimo_registro.año - 1
            año2 = ultimo_registro.año
        except:
            año1 = 1
            año2 = 2

        # Filtramos publicadores activos y en servicio
        publicadores = Publicador.objects.filter(grupo=grupo,estado="Activo",servicio__isnull=True)

        # Configuración PDF
        response = HttpResponse(content_type='application/pdf')
        response["Content-Disposition"] = f'inline; filename="Grupo {grupo}.pdf"'
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

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

        for pub in publicadores:
            # Título con el nombre del publicador
            story.append(Paragraph(f"REGISTRO DE PUBLICADOR DE LA CONGREGACION", titulo_modificado))
            story.append(Paragraph(f"Nombre: {pub.apellido}, {pub.nombre}", normal_modificado))
            story.append(Paragraph(f"Fecha nacimiento: {pub.nacimiento}", normal_modificado_izq))
            story.append(Paragraph(f"Fecha bautismo: {pub.bautismo}", normal_modificado_izq))
            story.append(Paragraph(f"Sexo: {pub.sexo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.u_oo}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.servicio}", normal_modificado_izq))
            story.append(Paragraph(f"{pub.a_sm}", normal_modificado_izq))
            story.append(Spacer(1, 12))


            # ====================
            # Función auxiliar para armar tabla de un año
            def build_table(año_actual):
                data = [[año_actual, "Participación", "Estudios", "Auxiliar", "Horas", "Notas"]]
                total_horas = 0

                # Traer registros ya ordenados según la BD
                informes = Informe.objects.filter(
                    publicador=pub,
                    año=año_actual
                ).order_by("id")   # o por el campo que asegura tu orden Sept→Ago

                for informe in informes:
                    participacion = informe.participacion or 0
                    estudios = informe.estudios or 0
                    auxiliar = informe.auxiliar or 0
                    horas = informe.horas or 0
                    notas = informe.notas or ""

                    total_horas += horas

                    # Convertir mes numérico a nombre
                    mes_nombre = MESES_SERVICIO.get(informe.mes, "")

                    data.append([mes_nombre, participacion, estudios, auxiliar, horas, notas])

                # Fila total de horas
                data.append(["Total", "", "", "", total_horas, ""])

                table = Table(data, colWidths=[90, 70, 50, 50, 50, 160])
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ]))
                return table


            # ====================
            # Tabla Año 1
            story.append(build_table(año1))
            story.append(Spacer(1, 20))

            # Tabla Año 2
            story.append(build_table(año2))

            # Nueva página por cada publicador
            story.append(PageBreak())

        # Generamos el PDF
        doc.build(story)
        return response



def publicadores_sin_informe(request,grupo):
    hoy = date.today()
    mes_actual = hoy.month
    anio_actual = hoy.year

    if mes_actual in range(10, 13):  # de 9 a 12 (septiembre a diciembre)
        anio_consulta = (anio_actual + 1)
    else:
        anio_consulta = (anio_actual)
    mes_consulta = mes_actual - 1 
    

    # --- Obtener publicadores que NO tienen informe de ese mes y año de servicio ---
    publicadores_con_informe = Informe.objects.filter(
        año=anio_consulta, mes=mes_consulta
    ).values_list("publicador_id", flat=True)

    publicadores_sin_informe = (
        Publicador.objects.filter(estado="Activo", grupo=grupo)
        .exclude(id__in=publicadores_con_informe)
        .order_by("grupo", "apellido", "nombre")
    )
    print(grupo)
    context = {
        "publicadores": publicadores_sin_informe.order_by("apellido", "nombre"),
        "mes_consulta": mes_consulta,
        "anio_servicio": anio_consulta,
        "grupo": grupo,
    }
    return render(request, "informe/publicadores_sin_informe.html", context)
