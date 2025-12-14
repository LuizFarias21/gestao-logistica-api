# frota/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MotoristaViewSet, AtribuirVeiculoAPIView

# 1. Cria o roteador para as rotas CRUD
router = DefaultRouter()
router.register("motoristas", MotoristaViewSet)  # Rota: /api/motoristas/ (CRUD)

urlpatterns = [
    # 2. Inclui todas as rotas do ModelViewSet (CRUD básico)
    path("", include(router.urls)),
    # 3. Rota Específica: PATCH /api/motoristas/{id}/atribuir-veiculo/
    path(
        "motoristas/<int:motorista_id>/atribuir-veiculo/",
        AtribuirVeiculoAPIView.as_view(),
        name="atribuir-veiculo",
    ),
    # 4. Rota Pendente: /api/motoristas/{id}/entregas/
    # path('motoristas/<int:pk>/entregas/', ...),
    # 5. Rota Pendente: /api/motoristas/{id}/rotas/
    # path('motoristas/<int:pk>/rotas/', ...),
]
