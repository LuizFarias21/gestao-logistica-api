from rest_framework import serializers
from .models import Rota


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

    class Meta:
        model = Rota
        fields = [
            "id",
            "nome",
            "status",
            "data_rota",
            "capacidade_total_utilizada",
            "km_total_estimado",
            "tempo_estimado",
            "motorista",
            "veiculo",
        ]
