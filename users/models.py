from django.db import models

class Users(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=50)


class HistoricoCompra(models.Model):
    itens = models.JSONField()  # guarda a lista de itens da compra como JSON
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField()  # data da compra vinda do frontend

    def __str__(self):
        return f"Compra em {self.data_compra} - Total: R$ {self.total}"