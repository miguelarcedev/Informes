from urllib import response
from django.shortcuts import render, HttpResponse



# Create your views here.

def home(request):
    
    return render(request, "Informes\startbootstrap-heroic-features\dist\index.html")


