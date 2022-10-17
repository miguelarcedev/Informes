from urllib import response
from django.shortcuts import render
from django.db.models import Sum, Count, Max

from publicador.models import Publicador

# Create your views here.

def home(request):

    grupos=Publicador.objects.filter(estado="Activo").values('grupo').order_by('grupo').annotate(suma=Sum('grupo'))

    return render(request, "home.html",{"grupos": grupos})
   
  

