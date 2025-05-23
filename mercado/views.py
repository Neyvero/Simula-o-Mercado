from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "mercado/index.html"


def index(request):
    return HttpResponse("Seja muito bem vindo ao meu site.")


def index(request):
    return render(request, "mercado/index.html")
