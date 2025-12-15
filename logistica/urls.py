from rest_framework.routers import DefaultRouter
from .views import RotaViewSet

router = DefaultRouter()
router.register(r"rotas", RotaViewSet, basename="rota")

urlpatterns = router.urls
