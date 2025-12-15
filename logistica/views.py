from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Rota, Entrega
from .serializers import (
    RotaSerializer,
    RotaStatusSerializer,
    RotaDashboardSerializer,
    AdicionarEntregaRotaSerializer,
)


class RotaViewSet(viewsets.ModelViewSet):
    """
    ViewSet responsável pelo gerenciamento das Rotas.
    Inclui:
    - CRUD completo
    - Dashboard da rota
    - Regra de capacidade ao adicionar entregas
    """

    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "motorista", "data_rota"]

    # Dashboard da Rota
    @action(detail=True, methods=["get"], url_path="dashboard")
    def dashboard(self, request, pk=None):
        rota = self.get_object()
        serializer = RotaDashboardSerializer(rota)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Adicionar entrega com validação de capacidade (Issue 7)
    @action(detail=True, methods=["post"], url_path="entregas")
    def adicionar_entrega(self, request, pk=None):
        rota = self.get_object()
        serializer = AdicionarEntregaRotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entrega_id = serializer.validated_data["entrega_id"]

        try:
            entrega = Entrega.objects.get(id=entrega_id)
        except Entrega.DoesNotExist:
            return Response(
                {"detail": "Entrega não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        nova_capacidade = rota.capacidade_total_utilizada + entrega.capacidade

        if nova_capacidade > rota.veiculo.capacidade_maxima:
            return Response(
                {"detail": "Capacidade do veículo excedida."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rota.entregas.add(entrega)
        rota.capacidade_total_utilizada = nova_capacidade
        rota.save()

        return Response(
            {"detail": "Entrega adicionada com sucesso."},
            status=status.HTTP_201_CREATED,
        )

    # Exclusão com regra de negócio
    def destroy(self, request, *args, **kwargs):
        rota = self.get_object()

        if rota.status == Rota.Status.CONCLUIDO:
            return Response(
                {"detail": "Não é possível excluir uma rota concluída."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().destroy(request, *args, **kwargs)
