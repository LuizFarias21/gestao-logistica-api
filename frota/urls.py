from django.urls import path
from .views import VeiculoCreateView, VeiculoListView, VeiculoDetailView

urlpatterns = [
    path("criar/", VeiculoCreateView.as_view(), name="criar-veiculo"),
    path("listar/", VeiculoListView.as_view(), name="listar-veiculos"),
    path("<int:pk>/", VeiculoDetailView.as_view(), name="detalhe-veiculo"),
]
