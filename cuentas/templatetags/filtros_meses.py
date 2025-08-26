from django import template

register = template.Library()

MESES_SERVICIO = {    
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

@register.filter
def mes_personalizado(numero_mes):
    """Convierte número de mes en nombre según el calendario personalizado."""
    return MESES_SERVICIO.get(numero_mes, "Mes inválido")
