from rest_framework import serializers
from .models import Motorista


class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        # Campos que serão exibidos na API
        fields = [
            "id",
            "nome",
            "cpf",
            "cnh",
            "telefone",
            "status",
            "veiculo_atual_id",
            "data_cadastro",
        ]
        read_only_fields = ["data_cadastro"]
