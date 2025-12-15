from django.db import models


class Motorista(models.Model):
    STATUS_CHOICES = (
        ("disponivel", "Disponível"),
        ("em_rota", "Em Rota"),
        ("inativo", "Inativo"),
    )

    nome = models.CharField(max_length=100, help_text="Digite o nome do motorista")

    cpf = models.CharField(
        max_length=11, unique=True, help_text="Digite o CPF sem ponto ou traço"
    )

    cnh = models.CharField(
        max_length=10, unique=True, help_text="Digite o CNH sem ponto ou traço"
    )

    telefone = models.CharField(
        max_length=20, help_text="Digite o telefone. Ex: (61) 91234-5678"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="disponivel",
        help_text="Selecione o status do motorista",
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora do cadastro do motorista"
    )

    veiculo_atual_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="ID do Veículo Atual",
        help_text="ID do veículo associado",
    )

    def __str__(self):
        return self.nome
