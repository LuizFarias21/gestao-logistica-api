from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import MotoristaViewSet, VeiculoViewSet, ClienteViewSet

router = DefaultRouter()

router.register(r"motoristas", MotoristaViewSet, basename="motorista")
router.register(r"veiculos", VeiculoViewSet, basename="veiculo")
router.register(r"clientes", ClienteViewSet, basename="cliente")
# router.register(r"entregas", EntregaViewSet)
# router.register(r"rotas", RotaViewSet)

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(router.urls)),
]
