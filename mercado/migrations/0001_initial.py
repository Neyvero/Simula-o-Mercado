# Generated by Django 4.2.21 on 2025-06-04 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_compra', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('historico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='mercado.historicocompra')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='mercado.carrinho')),
            ],
        ),
    ]
