from rest_framework import serializers
from .models import Rota, Entrega


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = ["id", "descricao", "capacidade", "status"]


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = [
            "id",
            "nome",
            "descricao",
            "motorista",
            "veiculo",
            "data_rota",
            "status",
            "capacidade_total_utilizada",
            "km_total_estimado",
            "tempo_estimado",
        ]
        read_only_fields = ["capacidade_total_utilizada"]


class RotaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = ["status"]


class RotaDashboardSerializer(serializers.ModelSerializer):
    motorista = serializers.StringRelatedField()
    veiculo = serializers.StringRelatedField()
    entregas = EntregaSerializer(many=True)

    capacidade_maxima_veiculo = serializers.DecimalField(
        source="veiculo.capacidade_maxima",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    capacidade_disponivel = serializers.SerializerMethodField()

    class Meta:
        model = Rota
        fields = [
            "id",
            "nome",
            "status",
            "data_rota",
            "motorista",
            "veiculo",
            "capacidade_maxima_veiculo",
            "capacidade_total_utilizada",
            "capacidade_disponivel",
            "km_total_estimado",
            "tempo_estimado",
            "entregas",
        ]

    def get_capacidade_disponivel(self, obj):
        return obj.veiculo.capacidade_maxima - obj.capacidade_total_utilizada


class AdicionarEntregaRotaSerializer(serializers.Serializer):
    entrega_id = serializers.IntegerField()
