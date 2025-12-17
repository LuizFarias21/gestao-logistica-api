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
        # TODO: Escrever os fields


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        # TODO: Escrever os fields


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        # TODO: Escrever os fields
