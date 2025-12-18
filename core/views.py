from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Cliente, Motorista, Veiculo, Rota, Entrega
from .serializers import (
    ClienteSerializer,
    MotoristaSerializer,
    RotaSerializer,
    EntregaSerializer,
    VeiculoSerializer,
)
from .permissions import IsGestor, IsMotorista, IsCliente
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Gerencia os Clientes.
    - Gestor: Pode cadastrar, listar todos e deletar.
    - Cliente: Pode ver apenas seu próprio perfil e atualizar dados básicos (telefone/endereço).
    """

    serializer_class = ClienteSerializer
    permission_classes = [IsGestor | IsCliente]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Cliente.objects.all()
        if hasattr(user, "cliente"):
            return Cliente.objects.filter(id=user.cliente.id)
        return Cliente.objects.none()


class MotoristaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Motoristas (CRUD).
    Apenas Gestores podem criar, editar ou ver a lista completa de motoristas.
    """

    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsGestor | IsMotorista]

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsMotorista],
    )
    def entregas(self, request, pk=None):
        motorista = self.get_object()

        entregas = Entrega.objects.filter(motorista=motorista)
        serializer = EntregaSerializer(entregas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[IsMotorista])
    def rotas(self, request, pk=None):
        motorista = self.get_object()

        rotas = Rota.objects.filter(motorista=motorista)
        serializer = RotaSerializer(rotas, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="atribuir-veiculo",
        permission_classes=[IsGestor],
    )
    def atribuir_veiculo(self, request, pk=None):
        motorista = self.get_object()
        veiculo = request.data.get("veiculo")

        if not veiculo:
            return Response(
                {"erro": "O campo 'veiculo' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        veiculo = get_object_or_404(Veiculo, id=veiculo)

        veiculo.motorista = motorista
        veiculo.save()

        return Response(
            {
                "mensagem": f"Veículo {veiculo.placa} vinculado ao motorista {motorista.nome} com sucesso!"
            },
            status=status.HTTP_200_OK,
        )


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

    serializer_class = RotaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_queryset(self):
        # TODO: Implementar lógica de filtragem.
        # 1. Se for Gestor (user.is_staff) -> Retornar tudo.
        # 2. Se for Motorista -> Retornar apenas Rota.objects.filter(motorista=user.motorista)
        pass


class EntregaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Entregas.
    Gestores: Acesso total.
    Motoristas: Atualizam status das entregas de suas rotas.
    Clientes: Visualizam apenas suas próprias entregas (somente leitura).
    """

    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    permission_classes = [IsGestor | IsMotorista | IsCliente]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Entrega.objects.all()

        if hasattr(user, "motorista"):
            return Entrega.objects.filter(motorista=user.motorista)

        if hasattr(user, "cliente"):
            return Entrega.objects.filter(cliente=user.cliente)

        return Entrega.objects.none()

    def perform_create(self, serializer):
        if not serializer.validated_data.get("endereco_origem"):
            raise ValidationError(
                {"endereco_origem": "O endereço de origem é obrigatório."}
            )

        if not serializer.validated_data.get("endereco_destino"):
            raise ValidationError(
                {"endereco_destino": "O endereço de destino é obrigatório."}
            )

        if not serializer.validated_data.get("cliente"):
            raise ValidationError({"cliente": "O cliente é obrigatório."})

        serializer.save()

    @extend_schema(
        summary="Atribuir Motorista",
        description="Vincula manualmente um motorista específico a esta entrega.",
        request={"type": "object", "properties": {"motorista_id": {"type": "integer"}}},
        responses={200: EntregaSerializer},
    )
    @action(detail=True, methods=["patch"])
    def atribuir_motorista(self, request, pk=None):
        entrega = self.get_object()
        motorista_id = request.data.get("motorista_id")

        if not motorista_id:
            return Response(
                {"erro": "O campo motorista_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            motorista = Motorista.objects.get(pk=motorista_id)
        except Motorista.DoesNotExist:
            return Response(
                {"erro": "Motorista não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        entrega.motorista = motorista
        entrega.save()

        serializer = self.get_serializer(entrega)
        return Response(serializer.data)

    @extend_schema(
        summary="Rastreamento da Entrega",
        description="Retorna informações de rastreamento da entrega, incluindo status e previsão de entrega.",
        responses={200: EntregaSerializer},
    )
    @action(detail=True, methods=["get"])
    def rastreamento(self, request, pk=None):
        entrega = self.get_object()
        serializer = self.get_serializer(entrega)

        return Response(
            {
                "codigo_rastreio": entrega.codigo_rastreio,
                "status": entrega.status,
                "data_entrega_prevista": entrega.data_entrega_prevista,
                "data_entrega_real": entrega.data_entrega_real,
                "endereco_origem": entrega.endereco_origem,
                "endereco_destino": entrega.endereco_destino,
            }
        )

    @extend_schema(
        summary="Marcar como Entregue",
        description="Atualiza o status da entrega para 'entregue' e registra a data de entrega real.",
        responses={200: EntregaSerializer},
    )
    @action(detail=True, methods=["patch"])
    def marcar_entregue(self, request, pk=None):
        entrega = self.get_object()

        if entrega.status == "entregue":
            return Response(
                {"erro": "Esta entrega já foi marcada como entregue."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        entrega.status = "entregue"
        entrega.data_entrega_real = timezone.now()
        entrega.save()

        serializer = self.get_serializer(entrega)
        return Response(serializer.data)
