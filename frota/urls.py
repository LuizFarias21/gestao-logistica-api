from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MotoristaViewSet,
    AtribuirVeiculoAPIView,
    MotoristaEntregasView
)

router = DefaultRouter()
router.register("motoristas", MotoristaViewSet)

urlpatterns = [
    # rotas do ViewSet
    path("", include(router.urls)),

    # rota para atribuir veículo
    path(
        "motoristas/<int:motorista_id>/atribuir-veiculo/",
        AtribuirVeiculoAPIView.as_view(),
        name="atribuir-veiculo",
    ),

    # ✅ rota pedida no PDF
    path(
        "motoristas/<int:id>/entregas/",
        MotoristaEntregasView.as_view(),
        name="motorista-entregas",
    ),
]
