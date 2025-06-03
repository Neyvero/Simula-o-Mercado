from rest_framework import serializers
from .models import HistoricoCompra, ItemCompra

class ItemCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ['id', 'descricao']

class HistoricoCompraSerializer(serializers.ModelSerializer):
    itens = ItemCompraSerializer(many=True)   # nested

    class Meta:
        model = HistoricoCompra
        fields = ['id', 'itens', 'total', 'data_compra']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        historico = HistoricoCompra.objects.create(**validated_data)
        for item_dict in itens_data:
            ItemCompra.objects.create(
                historico=historico,
                descricao=item_dict['descricao']
            )
        return historico
