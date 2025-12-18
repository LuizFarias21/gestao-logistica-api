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
)

router = DefaultRouter()

router.register(r"motoristas", MotoristaViewSet)
router.register(r"veiculos", VeiculoViewSet)


urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
    path("motoristas/<int:pk>/entregas/", MotoristaViewSet.as_view({"get": "entregas"}), name="motorista-entregas"),
   
    path("motoristas/<int:pk>/rotas/", MotoristaViewSet.as_view({"get": "rotas"}), name="motorista-rotas"),
    path("", include(router.urls)),
]
