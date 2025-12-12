from rest_framework import serializers
from .models import Veiculo


class VeiculoSerializer(serializers.ModelSerializer):
    motorista_username = serializers.CharField(
        source="motorista.username", read_only=True
    )

    class Meta:
        model = Veiculo
        fields = [
            "id",
            "placa",
            "modelo",
            "ano",
            "status",
            "motorista",
            "motorista_username",
        ]
