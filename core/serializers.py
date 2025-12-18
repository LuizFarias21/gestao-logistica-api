from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cliente, Motorista, Rota, Entrega, Veiculo


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # TODO: Escrever os fields


class MotoristaSerializer(serializers.ModelSerializer):
    # permite que o gestor informe um user (PK) ao criar um Motorista
    user = serializers.PrimaryKeyRelatedField(source="User", queryset=User.objects.all(), write_only=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(source="User", read_only=True)

    class Meta:
        model = Motorista
        fields = ["id", "user", "user_id", "nome", "cpf", "cnh", "telefone", "status", "data_cadastro"]


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        # TODO: Escrever os fields


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = ["id", "codigo_rastreio", "motorista"]


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = ["id", "nome", "motorista"]
