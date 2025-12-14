# frota/serializers.py
from rest_framework import serializers
from .models import Motorista  # 👈 ISSO É CRÍTICO: O Ponto ('.') indica que Motorista está no mesmo app (frota)

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        # Verifique se todos esses campos existem no seu models.py
        fields = ['id', 'nome', 'cpf', 'cnh', 'telefone', 'status', 'veiculo_atual_id', 'data_cadastro']
        read_only_fields = ['data_cadastro']