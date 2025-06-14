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
from django.http import JsonResponse
import logging
import asyncio
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


async def teste_view(request):
    logger.debug("Debug log ativado")
    logger.info("Info log ativado")
    logger.warning("Warning log ativado")
    logger.error("Error log ativado")
    logger.critical("Critical log ativado")

    # Simula processo assíncrono com delay de 2 segundos
    await asyncio.sleep(2)

    return JsonResponse({'status': 'ok', 'mensagem': 'Teste de async e logs executado com sucesso!'})


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
        cpf = self.request.query_params.get('cpf')
        if cpf:
            return Carrinho.objects.filter(cpf=cpf)
        return Carrinho.objects.none()


    def list(self, request):
        cpf = request.query_params.get('cpf')
        if not cpf:
            return Response({"erro": "CPF não informado"}, status=status.HTTP_400_BAD_REQUEST)

        carrinho, _ = Carrinho.objects.get_or_create(cpf=cpf)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)


    def create(self, request):
        cpf = request.data.get('cpf')
        if not cpf:
            return Response({"erro": "CPF não informado"}, status=status.HTTP_400_BAD_REQUEST)

        carrinho, _ = Carrinho.objects.get_or_create(cpf=cpf)
        serializer = ItemCarrinhoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(carrinho=carrinho)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def finalizar(self, request):
        cpf = request.query_params.get('cpf')
        if not cpf:
            return Response({"erro": "CPF não informado"}, status=status.HTTP_400_BAD_REQUEST)

        carrinho = get_object_or_404(Carrinho, cpf=cpf)
        itens = carrinho.itens.all()

        if not itens:
            return Response({'erro': 'Carrinho vazio.'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.quantidade * item.preco_unitario for item in itens)
        historico = HistoricoCompra.objects.create(
            total=total, data_compra=now())

        for item in itens:
            ItemCompra.objects.create(
                historico=historico, descricao=item.descricao)

        itens.delete()

        return Response(HistoricoCompraSerializer(historico).data)


    @action(detail=True, methods=['patch'])
    def atualizar_quantidade(self, request, pk=None):
        cpf = request.query_params.get('cpf')
        if not cpf:
            return Response({"erro": "CPF não informado"}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(ItemCarrinho, pk=pk, carrinho__cpf=cpf)
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
        cpf = request.query_params.get('cpf')
        if not cpf:
            return Response({"erro": "CPF não informado"}, status=status.HTTP_400_BAD_REQUEST)

        carrinho = Carrinho.objects.filter(cpf=cpf).first()
        if carrinho:
            carrinho.itens.all().delete()
            return Response({"mensagem": "Carrinho limpo com sucesso."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"erro": "Carrinho não encontrado."}, status=status.HTTP_404_NOT_FOUND)

def buscar_produto(request):
    termo = request.GET.get('q', '').strip().lower()

    produtos = [
        {'name': 'Alcatra', 'sessaoId': 'acougue'},
        {'name': 'Frango', 'sessaoId': 'acougue'},
        {'name': 'Picanha', 'sessaoId': 'acougue'},
        {'name': 'Cerveja', 'sessaoId': 'bebidas'},
        {'name': 'Água', 'sessaoId': 'bebidas'},
        {'name': 'Suco', 'sessaoId': 'bebidas'},
        {'name': 'Sabonete', 'sessaoId': 'higiene_pessoal'},
        {'name': 'Shampoo', 'sessaoId': 'higiene_pessoal'},
        {'name': 'Banana', 'sessaoId': 'hortifruti'},
        {'name': 'Maçã', 'sessaoId': 'hortifruti'},
        {'name': 'Tomate', 'sessaoId': 'hortifruti'},
        {'name': 'Uva', 'sessaoId': 'hortifruti'},
        {'name': 'Leite', 'sessaoId': 'laticinios'},
        {'name': 'Queijo', 'sessaoId': 'laticinios'},
        {'name': 'Detergente', 'sessaoId': 'limpeza'},
        {'name': 'Sabão em Pó', 'sessaoId': 'limpeza'},
        {'name': 'Vassoura', 'sessaoId': 'limpeza'},
        {'name': 'Arroz', 'sessaoId': 'mercearia'},
        {'name': 'Café', 'sessaoId': 'mercearia'},
        {'name': 'Feijão', 'sessaoId': 'mercearia'},
        {'name': 'Pão Francês', 'sessaoId': 'padaria'},
        {'name': 'Bolo', 'sessaoId': 'padaria'},
        {'name': 'Pão Francês', 'sessaoId': 'padaria'},
        {'name': 'Rosquinha', 'sessaoId': 'padaria'},
    ]

    paths = {
        'acougue': 'mercado:acougue',
        'bebidas': 'mercado:bebidas',
        'hortifruti': 'mercado:hortifruti',
        'limpeza': 'mercado:limpeza',
        'padaria': 'mercado:padaria',
        'mercearia': 'mercado:mercearia',
        'laticinios': 'mercado:laticinios',
        'higiene_pessoal': 'mercado:higiene_pessoal',
    }

    produto_encontrado = None
    for p in produtos:
        if termo in p['name'].lower():
            produto_encontrado = p
            break

    if not produto_encontrado:

        return redirect('mercado:index')

    sessao = produto_encontrado['sessaoId']
    if sessao not in paths:
        return redirect('mercado:index')

    return redirect(paths[sessao])