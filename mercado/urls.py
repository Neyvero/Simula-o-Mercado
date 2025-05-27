from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HistoricoCompraViewSet
from . import views

app_name = "mercado"

router = DefaultRouter()
router.register(r'historico', HistoricoCompraViewSet)

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),          # view normal da homepage
    path("api/", include(router.urls)),                         # API REST do mercado
]
