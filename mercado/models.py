from django.db import models
from django.contrib.auth.models import User

class HistoricoCompra(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2) # soma da compra
    data_compra = models.DateTimeField() # data da compra

    def __str__(self):
        return f"Compra em {self.data_compra} - Total: R$ {self.total}" # retorna para o usuário

#integração para o banco de dados
class ItemCompra(models.Model):
    historico = models.ForeignKey(
        HistoricoCompra,
        related_name='itens',    
        on_delete=models.CASCADE
    )
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.descricao} (Compra #{self.historico_id})"
    
class Carrinho(models.Model):
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,   
        null=True, 
        blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    teste_temp = models.BooleanField(default=False)

    def __str__(self):
        return f"Carrinho de {self.usuario}"

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    descricao = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
