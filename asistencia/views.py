from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic.list import ListView
from django.http import  HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from asistencia.models import *
from django.views.generic import  View
from django.utils import timezone
from django.db.models import Sum

# Create your views here.



class EntreSemanaListView(ListView):

    model = Entre_Semana
    template_name = 'asistencia/lista.html'
    paginate_by = 12  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class Entre_SemanaListView(ListView):

    model = Entre_Semana
    template_name = 'asistencia/lista.html'
    paginate_by = 12  # if pagination is desired


def Entre_Semana_list(request, año):
    años=Entre_Semana.objects.filter(año=año)
    return render(request, "asistencia/lista_por_año.html",{"años": años, "anio":año})


def Entre_Semana_años(request):
    años=Entre_Semana.objects.values('año').order_by('año').annotate(suma=Sum('cantidad'))
    return render(request, "asistencia/lista_años.html",{"años": años})
    

class EntreSemanaPdf(View):

    def get(self, request,año, *args, **kwargs):
        
        
        template = get_template('asistencia/EntreSemana.html')
        context = {'asistencia': Entre_Semana.objects.filter(año=año)}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
       
        return response
        
class FinDeSemanaPdf(View):

    def get(self, request, *args, **kwargs):
        
        
        template = get_template('asistencia/FinDeSemana.html')
        context = {'asistencia': Fin_De_Semana.objects.all}
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        return response