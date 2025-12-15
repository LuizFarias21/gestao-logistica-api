from rest_framework import serializers
from .models import Motorista


class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = "__all__"
        read_only_fields = ["data_cadastro"]
