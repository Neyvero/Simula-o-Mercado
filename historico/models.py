from django.db import models

class HistoricoCompra(models.Model):
    itens = models.JSONField()  # lista dos itens comprados
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra em {self.data_compra} - Total: R$ {self.total}"
