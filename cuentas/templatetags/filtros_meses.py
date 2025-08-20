from django import template

register = template.Library()

MESES_SERVICIO = {
    1: "Septiembre",
    2: "Octubre",
    3: "Noviembre",
    4: "Diciembre",
    5: "Enero",
    6: "Febrero",
    7: "Marzo",
    8: "Abril",
    9: "Mayo",
    10: "Junio",
    11: "Julio",
    12: "Agosto",
}

@register.filter
def mes_personalizado(numero_mes):
    """Convierte número de mes en nombre según el calendario personalizado."""
    return MESES_SERVICIO.get(numero_mes, "Mes inválido")
