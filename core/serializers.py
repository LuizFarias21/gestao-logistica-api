from rest_framework import serializers
from .models import Cliente, Motorista, Rota, Entrega, Veiculo


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # TODO: Escrever os fields


class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = "__all__"


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = "__all__"


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = [
            "id",
            "codigo_rastreio",
            "capacidade",
            "status",
            "motorista",
        ]


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
            "entregas",
        ]


class RotaDashboardSerializer(serializers.ModelSerializer):
    motorista = MotoristaSerializer(read_only=True)
    veiculo = VeiculoSerializer(read_only=True)
    entregas = EntregaSerializer(many=True, read_only=True)

    class Meta:
        model = Rota
        fields = [
            "id",
            "nome",
            "descricao",
            "status",
            "data_rota",
            "capacidade_total_utilizada",
            "km_total_estimado",
            "tempo_estimado",
            "motorista",
            "veiculo",
            "entregas",
        ]

    def get_capacidade_disponivel(self, obj):
        return obj.veiculo.capacidade_maxima - obj.capacidade_total_utilizada
