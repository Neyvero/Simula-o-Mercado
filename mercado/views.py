from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import viewsets
from .models import HistoricoCompra
from .serializers import HistoricoCompraSerializer


class IndexView(TemplateView):
    template_name = "mercado/index.html"


def index(request):
    return HttpResponse("Seja muito bem vindo ao meu site.")


def index(request):
    return render(request, "mercado/index.html")


def acougue(request):
    return render(request, 'mercado/acougue.html')


def bebidas(request):
    return render(request, 'mercado/bebidas.html')


def higiene_pessoal(request):
    return render(request, 'mercado/higiene_pessoal.html')


def hortifruti(request):
    return render(request, 'mercado/hortifruti.html')


def laticinios(request):
    return render(request, 'mercado/laticinios.html')


def limpeza(request):
    return render(request, 'mercado/limpeza.html')


def mercearia(request):
    return render(request, 'mercado/mercearia.html')


def padaria(request):
    return render(request, 'mercado/padaria.html')


class HistoricoCompraViewSet(viewsets.ModelViewSet):
    queryset = HistoricoCompra.objects.all().order_by('-data_compra')
    serializer_class = HistoricoCompraSerializer
