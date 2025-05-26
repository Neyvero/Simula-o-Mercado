from rest_framework.routers import DefaultRouter
from .views import HistoricoCompraViewSet

router = DefaultRouter()
router.register(r'historico', HistoricoCompraViewSet)

urlpatterns = router.urls
