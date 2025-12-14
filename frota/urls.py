from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MotoristaViewSet, AtribuirVeiculoAPIView

# O Router cuida das rotas de CRUD (listar, criar, detalhar, atualizar, deletar)
router = DefaultRouter()
router.register(r'motoristas', MotoristaViewSet)

urlpatterns = [
    # Inclui todas as rotas do ModelViewSet (CRUD básico)
    path('', include(router.urls)), 
    
    # Rota Específica: PATCH /api/motoristas/{id}/atribuir-veiculo/
    path(
        'motoristas/<int:motorista_id>/atribuir-veiculo/', 
        AtribuirVeiculoAPIView.as_view(), 
        name='atribuir-veiculo'
    ),
    
    # ROTAS PENDENTES (Dependem dos modelos de Entrega/Rota):
    # path('motoristas/<int:pk>/entregas/', ... ),  # GET /api/motoristas/{id}/entregas/
    # path('motoristas/<int:pk>/rotas/', ... ),     # GET /api/motoristas/{id}/rotas/
]