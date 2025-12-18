from rest_framework import serializers
from .models import Cliente, Motorista, Rota, Entrega, Veiculo


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["endereco", "telefone"]
        read_only_fields = ["nome", "user"]


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
        # TODO: Escrever os fields


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = "__all__"
