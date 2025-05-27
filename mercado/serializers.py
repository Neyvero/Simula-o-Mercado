from rest_framework import serializers
from .models import HistoricoCompra

class HistoricoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoCompra
        fields = '__all__'
