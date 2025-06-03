from rest_framework import viewsets
from .models import HistoricoCompra
from .serializers import HistoricoCompraSerializer
from django.http import JsonResponse
from .models import Users
from mercado.models import HistoricoCompra


class HistoricoCompraViewSet(viewsets.ModelViewSet):
    queryset = HistoricoCompra.objects.all().order_by('-data_compra')
    serializer_class = HistoricoCompraSerializer


def all_user(request):
    users = list(Users.objects.values('id', 'email'))
    return JsonResponse(users, safe=False)

