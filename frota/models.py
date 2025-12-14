from django.db import models


class Motorista(models.Model):
    # Status de acordo com o requisito (inativo, em_rota, disponível)
    STATUS_CHOICES = (
        ("disponivel", "Disponível"),
        ("em_rota", "Em Rota"),
        ("inativo", "Inativo"),
    )

    # Campos Obrigatórios com regras de Unicidade
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)  # CPF deve ser único
    cnh = models.CharField(max_length=10, unique=True)  # CNH deve ser única
    telefone = models.CharField(max_length=20)

    # Status
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="disponivel"
    )

    # Data de Cadastro
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # Relação com Veículo (1:1, nullable)
    # unique=True garante que apenas um motorista por vez pode ter esse veiculo_id.
    veiculo_atual_id = models.IntegerField(
        null=True, blank=True, unique=True, verbose_name="ID do Veículo Atual"
    )

    def __str__(self):
        return self.nome
