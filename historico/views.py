from rest_framework import viewsets
from .models import HistoricoCompra
from .serializers import HistoricoCompraSerializer

class HistoricoCompraViewSet(viewsets.ModelViewSet):
    queryset = HistoricoCompra.objects.all().order_by('-data_compra')
    serializer_class = HistoricoCompraSerializer
