from django.db import connection
from shared.models import Congregacion
from publicador.models import Publicador
from informe.models import Informe

def get_schema_name():
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_schema()")
        schema_name = cursor.fetchone()[0]
    
    congregacion = Congregacion.objects.filter(schema_name=schema_name)
    
    return congregacion

def calculo_irregulares():
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
        return(irregulares, cantidad)

def calculo_inactivos():
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
        return(irregulares, cantidad)
    