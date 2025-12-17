from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cliente, Motorista, Veiculo, Rota, Entrega
from .serializers import (
    ClienteSerializer,
    MotoristaSerializer,
    RotaSerializer,
    RotaDashboardSerializer,
    EntregaSerializer,
    VeiculoSerializer,
)
from .permissions import IsGestor, IsMotorista, IsCliente
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Clientes.
    Apenas Gestores podem cadastrar ou ver a lista de clientes.
    Clientes comuns não precisam acessar esse endpoint (eles acessam /api/entregas/).
    """

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsGestor]


class MotoristaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Motoristas (CRUD).
    Apenas Gestores podem criar, editar ou ver a lista completa de motoristas.
    """

    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsGestor]


class VeiculoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo da frota de veículos.

    Apenas usuários com perfil de **Gestor** podem criar, editar ou excluir veículos.
    """

    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsGestor]

    @extend_schema(
        summary="Listar Veículos Disponíveis",
        description="Retorna uma lista filtrada contendo apenas os veículos que estão com o status **'DISPONIVEL'** no momento.",
        responses={200: VeiculoSerializer(many=True)},
    )
    @action(detail=False)
    def disponiveis(self, request):
        disponiveis = Veiculo.objects.filter(status="DISPONIVEL")
        serializer = self.get_serializer(disponiveis, many=True)

        return Response(serializer.data)

    @extend_schema(
        summary="Obter Histórico de Rotas",
        description="Recupera todas as rotas (histórico de viagens) vinculadas a este veículo específico.",
        responses={200: RotaSerializer(many=True)},
    )
    @action(detail=True)
    def rotas(self, request, pk=None):
        veiculo = self.get_object()
        serializer = RotaSerializer(veiculo.rotas.all(), many=True)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        """
        Sobrescreve a exclusão padrão para checar se há rotas em andamento.
        """
        if instance.rotas.filter(status="EM_ANDAMENTO").exists():
            raise ValidationError(
                "Não é possível excluir este veículo pois ele está vinculado a uma rota em andamento."
            )

        super().perform_destroy(instance)


class RotaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Rotas.
    Gestores: Acesso total.
    Motoristas: Visualizam apenas suas próprias rotas.
    """

    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_queryset(self):
        user = self.request.user

        # Gestor vê tudo
        if user.is_staff:
            return Rota.objects.all()

        # Motorista vê apenas suas rotas
        if hasattr(user, "motorista"):
            return Rota.objects.filter(motorista=user.motorista)

        return Rota.objects.none()

    @extend_schema(
        summary="Dashboard da Rota",
        description="Retorna dados completos da rota, motorista, veículo e entregas.",
        responses={200: RotaDashboardSerializer},
    )
    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        rota = self.get_object()
        serializer = RotaDashboardSerializer(rota)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def entregas(self, request, pk=None):
        rota = self.get_object()
        entrega_id = request.data.get("entrega_id")

        if not entrega_id:
            raise ValidationError("Informe o ID da entrega.")

        try:
            entrega = Entrega.objects.get(id=entrega_id)
        except Entrega.DoesNotExist:
            raise ValidationError("Entrega não encontrada.")

        nova_capacidade = rota.capacidade_total_utilizada + entrega.capacidade

        if nova_capacidade > rota.veiculo.capacidade_maxima:
            raise ValidationError(
                "Capacidade do veículo excedida ao adicionar esta entrega."
            )

        rota.entregas.add(entrega)
        rota.capacidade_total_utilizada = nova_capacidade
        rota.save()

        return Response({"detail": "Entrega adicionada com sucesso à rota."})

    def perform_destroy(self, instance):
        if instance.status == "CONCLUIDO":
            raise ValidationError("Não é possível excluir uma rota já concluída.")
        super().perform_destroy(instance)


class EntregaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Entregas.
    Gestores: Acesso total.
    Motoristas: Atualizam status das entregas de suas rotas.
    Clientes: Visualizam apenas suas próprias entregas (somente leitura).
    """

    serializer_class = EntregaSerializer
    permission_classes = [IsGestor | IsMotorista | IsCliente]

    def get_queryset(self):
        user = self.request.user

        # Gestor vê tudo
        if user.is_staff:
            return Entrega.objects.all()

        # Motorista vê entregas das suas rotas
        if hasattr(user, "motorista"):
            return Entrega.objects.filter(rota__motorista=user.motorista).distinct()

        # Cliente vê apenas suas próprias entregas
        if hasattr(user, "cliente"):
            return Entrega.objects.filter(cliente=user.cliente)

        return Entrega.objects.none()
