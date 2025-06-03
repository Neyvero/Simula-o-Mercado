from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils.timezone import now
from django.views.generic import TemplateView
from .models import HistoricoCompra, Carrinho, ItemCompra, ItemCarrinho
from .serializers import HistoricoCompraSerializer, ItemCarrinhoSerializer, CarrinhoSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


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


class CarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = CarrinhoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Carrinho.objects.filter(usuario=user)
        else:
            return Carrinho.objects.none()

    def list(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"erro": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        carrinho, _ = Carrinho.objects.get_or_create(usuario=user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"erro": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        carrinho, _ = Carrinho.objects.get_or_create(usuario=user)
        serializer = ItemCarrinhoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(carrinho=carrinho)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def finalizar(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"erro": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        carrinho = get_object_or_404(Carrinho, usuario=user)
        itens = carrinho.itens.all()

        if not itens:
            return Response({'erro': 'Carrinho vazio.'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.quantidade * item.preco_unitario for item in itens)
        historico = HistoricoCompra.objects.create(
            total=total, data_compra=now())

        for item in itens:
            ItemCompra.objects.create(
                historico=historico, descricao=item.descricao)

        itens.delete()  # limpa o carrinho

        return Response(HistoricoCompraSerializer(historico).data)

    @action(detail=True, methods=['patch']) 
    def atualizar_quantidade(self, request, pk=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"erro": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        item = get_object_or_404(ItemCarrinho, pk=pk, carrinho__usuario=user)
        nova_qt = request.data.get("quantidade")

        if nova_qt is None:
            return Response({"erro": "Quantidade inválida"}, status=status.HTTP_400_BAD_REQUEST)

        nova_qt = int(nova_qt)
        if nova_qt < 1:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        item.quantidade = nova_qt
        item.save()
        return Response(ItemCarrinhoSerializer(item).data)
    
    @action(detail=False, methods=['delete'])
    def limpar(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"erro": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        carrinho = Carrinho.objects.filter(usuario=user).first()
        if carrinho:
            carrinho.itens.all().delete()
            return Response({"mensagem": "Carrinho limpo com sucesso."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"erro": "Carrinho não encontrado."}, status=status.HTTP_404_NOT_FOUND)
