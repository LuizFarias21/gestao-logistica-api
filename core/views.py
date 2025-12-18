from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal

from .models import Cliente, Motorista, Veiculo, Rota, Entrega
from .serializers import (
    ClienteSerializer,
    MotoristaSerializer,
    RotaSerializer,
    EntregaSerializer,
    EntregaMotoristaUpdateSerializer,
    VeiculoSerializer,
    EntregaClienteSerializer,
    AtribuirVeiculoRequestSerializer,
    AtribuirMotoristaRequestSerializer,
    AtribuirEntregasRotaRequestSerializer,
    MensagemResponseSerializer,
    RotaDashboardResponseSerializer,
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
    - Listar/Criar/Deletar: Apenas Gestores.
    - Detalhes (Retrieve): Gestores ou o próprio Motorista.
    """

    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_permissions(self):
        """
        Define permissões específicas para cada ação.
        """
        if self.action in ["list", "create", "destroy"]:
            return [IsGestor()]

        return super().get_permissions()

    @extend_schema(
        summary="Listar Entregas do Motorista",
        description="Retorna todas as entregas vinculadas ao motorista informado.",
        responses={200: EntregaSerializer(many=True)},
    )
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

    @extend_schema(
        summary="Listar Rotas do Motorista",
        description="Retorna todas as rotas vinculadas ao motorista informado.",
        responses={200: RotaSerializer(many=True)},
    )
    @action(detail=True, methods=["get"], permission_classes=[IsMotorista])
    def rotas(self, request, pk=None):
        motorista = self.get_object()
        rotas = Rota.objects.filter(motorista=motorista)
        serializer = RotaSerializer(rotas, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Atribuir Veículo ao Motorista (Gestor)",
        description="Vincula um veículo existente a um motorista.",
        request=AtribuirVeiculoRequestSerializer,
        responses={200: MensagemResponseSerializer},
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="atribuir-veiculo",
        permission_classes=[IsGestor],
    )
    def atribuir_veiculo(self, request, pk=None):
        motorista = self.get_object()
        veiculo_id = request.data.get("veiculo")

        if not veiculo_id:
            return Response(
                {"erro": "O campo 'veiculo' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        veiculo = get_object_or_404(Veiculo, id=veiculo_id)
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
    - Gestores: Acesso total (CRUD).
    - Motoristas: Visualizam apenas suas próprias rotas.
    """

    serializer_class = RotaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Rota.objects.all()

        if hasattr(user, "motorista"):
            return Rota.objects.filter(motorista=user.motorista)

        return Rota.objects.none()

    @extend_schema(
        summary="Dashboard da Rota (Visão Completa)",
        description="Retorna a composição completa: Dados da Rota, Motorista, Veículo e lista de Entregas.",
        responses={200: RotaDashboardResponseSerializer},
    )
    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        rota = self.get_object()

        entregas = rota.entregas.all()

        total_entregas = entregas.count()
        entregas_concluidas = entregas.filter(status="entregue").count()

        data = {
            "rota": {
                "id": rota.id,
                "nome": rota.nome,
                "status": rota.status,
                "data": rota.data_rota,
            },
            "motorista": {
                "nome": rota.motorista.nome,
                "telefone": rota.motorista.telefone,
            },
            "veiculo": {
                "modelo": rota.veiculo.modelo,
                "placa": rota.veiculo.placa,
                "capacidade_maxima": rota.veiculo.capacidade_maxima,
            },
            "progresso": {
                "total_entregas": total_entregas,
                "concluidas": entregas_concluidas,
                "pendentes": total_entregas - entregas_concluidas,
            },
            "entregas": [
                {
                    "codigo": e.codigo_rastreio,
                    "endereco": e.endereco_destino,
                    "status": e.status,
                }
                for e in entregas
            ],
        }
        return Response(data)

    @extend_schema(
        summary="Atribuir Entregas à Rota (com validação de capacidade)",
        description=(
            "Vincula uma ou mais entregas à rota e valida a regra: "
            "Soma(capacidade_necessaria) ≤ capacidade_maxima do veículo. "
            "As entregas são vinculadas também ao motorista da rota."
        ),
        request=AtribuirEntregasRotaRequestSerializer,
        responses={200: MensagemResponseSerializer},
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="atribuir-entregas",
        permission_classes=[IsGestor],
    )
    def atribuir_entregas(self, request, pk=None):
        rota = self.get_object()

        serializer = AtribuirEntregasRotaRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        codigos = serializer.validated_data["entregas"]

        capacidade_maxima = rota.veiculo.capacidade_maxima
        capacidade_atual = Entrega.objects.filter(rota=rota).aggregate(
            total=Sum("capacidade_necessaria")
        ).get("total") or Decimal("0")

        with transaction.atomic():
            for codigo in codigos:
                entrega = get_object_or_404(Entrega, codigo_rastreio=codigo)

                if entrega.rota_id and entrega.rota_id != rota.id:
                    raise ValidationError(
                        {
                            "entregas": (
                                f"A entrega {codigo} já está atribuída a outra rota (id={entrega.rota_id})."
                            )
                        }
                    )

                nova_capacidade = capacidade_atual + entrega.capacidade_necessaria
                if nova_capacidade > capacidade_maxima:
                    raise ValidationError(
                        {
                            "entregas": (
                                "Capacidade do veículo excedida ao atribuir entregas à rota. "
                                f"Capacidade máxima: {capacidade_maxima}. "
                                f"Capacidade atual: {capacidade_atual}. "
                                f"Tentando adicionar entrega {codigo} (capacidade {entrega.capacidade_necessaria})."
                            )
                        }
                    )

                entrega.rota = rota
                entrega.motorista = rota.motorista
                entrega.save(update_fields=["rota", "motorista"])
                capacidade_atual = nova_capacidade

        return Response(
            {
                "mensagem": (
                    f"{len(codigos)} entrega(s) atribuída(s) à rota {rota.id} com sucesso. "
                    f"Capacidade utilizada: {capacidade_atual}/{capacidade_maxima}."
                )
            },
            status=status.HTTP_200_OK,
        )


class EntregaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Entregas.
    - URL Principal: /api/entregas/{codigo_rastreio}/
    - Rastreamento: /api/entregas/{codigo_rastreio}/rastreamento/
    - Clientes: Veem apenas status e previsão (via Serializer Personalizado).
    """

    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    permission_classes = [IsGestor | IsMotorista | IsCliente]

    lookup_field = "codigo_rastreio"

    def get_serializer_class(self):
        """
        Define qual serializer usar baseado no perfil do usuário.
        """

        if hasattr(self.request.user, "cliente") and not self.request.user.is_staff:
            return EntregaClienteSerializer

        if hasattr(self.request.user, "motorista") and not self.request.user.is_staff:
            if self.action in ["update", "partial_update"]:
                return EntregaMotoristaUpdateSerializer
            if self.action in ["marcar_entregue"]:
                return EntregaSerializer

        return EntregaSerializer

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
        summary="Atribuir Motorista (Gestor)",
        description="Vincula manualmente um motorista a esta entrega.",
        request=AtribuirMotoristaRequestSerializer,
        responses={200: EntregaSerializer},
    )
    @action(detail=True, methods=["patch"], permission_classes=[IsGestor])
    def atribuir_motorista(self, request, codigo_rastreio=None):
        entrega = self.get_object()
        motorista_id = request.data.get("motorista_id")

        if not motorista_id:
            return Response({"erro": "ID do motorista obrigatório."}, status=400)

        motorista = get_object_or_404(Motorista, pk=motorista_id)
        entrega.motorista = motorista
        entrega.save()

        return Response(self.get_serializer(entrega).data)

    @extend_schema(
        summary="Marcar como Entregue (Motorista)",
        description="Atualiza status para 'entregue' e data real.",
        request=None,
        responses={200: EntregaSerializer},
    )
    @action(detail=True, methods=["patch"], permission_classes=[IsGestor | IsMotorista])
    def marcar_entregue(self, request, codigo_rastreio=None):
        entrega = self.get_object()

        if not request.user.is_staff:
            if entrega.motorista != request.user.motorista:
                return Response(
                    {"erro": "Você não é o motorista responsável por esta entrega."},
                    status=403,
                )

        if entrega.status == "entregue":
            return Response({"erro": "Entrega já finalizada."}, status=400)

        entrega.status = "entregue"
        entrega.data_entrega_real = timezone.now()
        entrega.save()

        return Response(self.get_serializer(entrega).data)

    @extend_schema(
        summary="Rastreamento da Entrega",
        description="Retorna informações de rastreamento.",
        responses={200: EntregaSerializer},
    )
    @action(detail=True, methods=["get"])
    def rastreamento(self, request, codigo_rastreio=None):
        entrega = self.get_object()
        serializer = self.get_serializer(entrega)
        return Response(serializer.data)
