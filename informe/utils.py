
from publicador.models import Publicador
from informe.models import Informe
from datetime import datetime

def calculo_irregulares():
        # Fecha y hora actual
        hoy = datetime.now()
        mes_actual = hoy.month   # número de mes (1-12)
        año_actual = hoy.year    # año (ej. 2025)
        
        if mes_actual in range(3, 9):  # de 3 a 8 (marzo a agosto)
            año = año_actual
        else:
            año = (año_actual -1, año_actual)

        bandera = True
        cantidad = 0
        key = []
        irregulares = []
        publicador = Publicador.objects.filter(estado="Activo").order_by('id')
        for p in publicador:
            key.append(p.id)
            
        for k in key:
            informe = Informe.objects.filter(publicador=k).order_by('-id')[0:6]
            bandera = True
            for i in informe:
                if isinstance(año, tuple):  # si 'año' tiene dos posibles valores
                    if i.año in año:
                        if i.participacion == "No":
                            irregulares.append((i.publicador,i.año,i.mes))
                            if bandera:
                                cantidad += 1
                                bandera = False
                else:
                     if i.año == año:
                        if i.participacion == "No":
                            irregulares.append((i.publicador,i.año,i.mes))
                            if bandera:
                                cantidad += 1
                                bandera = False
                     
        return(irregulares, cantidad)



def calculo_inactivos():
        año = 0
        orden = 0
        cantidad = 0
        key = []
        meses = ['Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto']
        publicador = Publicador.objects.filter(estado="Inactivo").order_by('id')
        for p in publicador:
            key.append(p.id)
        ultimo_registro = Informe.objects.last()    
        mes = ultimo_registro.mes
        for m in meses:
            orden += 1
            if m == mes:
                break
        if orden >= 5:
             año = ultimo_registro.año
        else:
             año = ultimo_registro.año - 1     
        for k in key:
            informe = Informe.objects.filter(publicador=k, año__gte=año).order_by('-id')[0:6]
            contador = 0
            for i in informe:
                if i.horas == 0:
                    contador += 1
                if contador == 6:
                    cantidad += 1             
        return(cantidad)

    
def nuevo(notas):
       
        cantidad = 0
        key = []
        publicador = Publicador.objects.filter(estado="Activo").order_by('id')
        for p in publicador:
            key.append(p.id)    
        for k in key:
            informe = Informe.objects.filter(publicador=k).order_by('-id')[0:6]
            
            for i in informe:
                if i.notas == notas:
                    cantidad += 1
                    break                           
        return(cantidad)

