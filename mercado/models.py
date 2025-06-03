from django.db import models

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
