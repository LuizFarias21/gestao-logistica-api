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