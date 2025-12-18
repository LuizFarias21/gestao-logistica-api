from decimal import Decimal

from django.db.models import Sum
from rest_framework import serializers
from .models import Cliente, Motorista, Rota, Entrega, Veiculo


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nome", "endereco", "telefone"]
        read_only_fields = ["user"]


class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = ["id", "nome", "cpf", "cnh", "telefone", "status"]


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = "__all__"


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = "__all__"
        read_only_fields = ["data_solicitacao"]

    def validate(self, attrs):
        """Impede associar/alterar entregas em rotas que excedam a capacidade do veículo."""

        instance = getattr(self, "instance", None)

        rota = attrs.get("rota")
        if rota is None and instance is not None:
            rota = instance.rota

        capacidade_necessaria = attrs.get("capacidade_necessaria")
        if capacidade_necessaria is None and instance is not None:
            capacidade_necessaria = instance.capacidade_necessaria

        if rota is None or capacidade_necessaria is None:
            return attrs

        qs = Entrega.objects.filter(rota=rota)
        if instance is not None and instance.pk:
            qs = qs.exclude(pk=instance.pk)

        capacidade_atual = qs.aggregate(total=Sum("capacidade_necessaria")).get(
            "total"
        ) or Decimal("0")
        capacidade_maxima = rota.veiculo.capacidade_maxima

        if capacidade_atual + capacidade_necessaria > capacidade_maxima:
            raise serializers.ValidationError(
                {
                    "rota": (
                        "Capacidade do veículo excedida para esta rota. "
                        f"Capacidade máxima: {capacidade_maxima}. "
                        f"Capacidade já utilizada: {capacidade_atual}. "
                        f"Capacidade desta entrega: {capacidade_necessaria}."
                    )
                }
            )

        return attrs


class EntregaMotoristaUpdateSerializer(serializers.ModelSerializer):
    """Serializer restrito para motorista: permite alterar apenas status/observações."""

    class Meta:
        model = Entrega
        fields = ["status", "observacoes"]


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = "__all__"
        read_only_fields = ["data_rota"]


class EntregaClienteSerializer(serializers.ModelSerializer):
    """
    Serializer restrito para visão do Cliente.
    Mostra apenas identificação, status e previsão.
    """

    class Meta:
        model = Entrega
        fields = ["codigo_rastreio", "status", "data_entrega_prevista"]


class AtribuirVeiculoRequestSerializer(serializers.Serializer):
    veiculo = serializers.IntegerField(help_text="ID do veículo a ser vinculado")


class AtribuirMotoristaRequestSerializer(serializers.Serializer):
    motorista_id = serializers.IntegerField(help_text="ID do motorista a ser vinculado")


class AtribuirEntregasRotaRequestSerializer(serializers.Serializer):
    entregas = serializers.ListField(
        child=serializers.CharField(),
        help_text="Lista de códigos de rastreio (codigo_rastreio) das entregas a serem atribuídas à rota",
        allow_empty=False,
    )


class MensagemResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField()


class RotaDashboardEntregaItemSerializer(serializers.Serializer):
    codigo = serializers.CharField(help_text="Código de rastreio")
    endereco = serializers.CharField(help_text="Endereço de destino")
    status = serializers.CharField(help_text="Status atual")


class RotaDashboardResponseSerializer(serializers.Serializer):
    rota = serializers.DictField(help_text="Dados básicos da rota")
    motorista = serializers.DictField(help_text="Dados do motorista")
    veiculo = serializers.DictField(help_text="Dados do veículo")
    progresso = serializers.DictField(help_text="Indicadores de progresso")
    entregas = RotaDashboardEntregaItemSerializer(many=True)
