from django.db import connection
from shared.models import Congregacion


def nombre(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_schema()")
        schema_name = cursor.fetchone()[0]
    
    congregacion = Congregacion.objects.filter(schema_name=schema_name)
    
    return {'nombre_cong': congregacion[0]}

