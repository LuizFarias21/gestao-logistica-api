from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import (
    MotoristaViewSet,
    VeiculoViewSet,
    RotaViewSet,
    EntregaViewSet,
    ClienteViewSet,
)

router = DefaultRouter()

router.register(r"motoristas", MotoristaViewSet)
router.register(r"veiculos", VeiculoViewSet)
router.register(r"rotas", RotaViewSet)
router.register(r"entregas", EntregaViewSet)
router.register(r"clientes", ClienteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
