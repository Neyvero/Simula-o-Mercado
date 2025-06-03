from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HistoricoCompraViewSet
from . import views

app_name = "mercado"

router = DefaultRouter()
router.register(r'historico', HistoricoCompraViewSet)

urlpatterns = [
    # view normal da homepage
    path("", views.IndexView.as_view(), name="index"),
    # API REST do mercado
    path("api/", include(router.urls)),
    path("mercado/acougue", views.acougue, name="acougue"),
    path("mercado/bebidas", views.bebidas, name="bebidas"),
    path("mercado/higiene_pessoal", views.higiene_pessoal, name="higiene_pessoal"),
    path("mercado/hortifruti", views.hortifruti, name="hortifruti"),
    path("mercado/laticinios", views.laticinios, name="laticinios"),
    path("mercado/limpeza", views.limpeza, name="limpeza"),
    path("mercado/mercearia", views.mercearia, name="mercearia"),
    path("mercado/padaria", views.padaria, name="padaria"),
]
