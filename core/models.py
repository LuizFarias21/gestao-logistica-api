from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    # TODO: Implementar model Cliente (Não se esquecer de associar com User)
    pass


class Motorista(models.Model):
    STATUS_CHOICES = (
        ("disponivel", "Disponível"),
        ("em_rota", "Em Rota"),
        ("inativo", "Inativo"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="motorista"
    )

    nome = models.CharField(max_length=100, help_text="Nome do motorista")

    cpf = models.CharField(
        max_length=11, unique=True, help_text="CPF sem ponto ou traço"
    )

    cnh = models.CharField(
        max_length=11, unique=True, help_text="CNH sem ponto ou traço"
    )

    telefone = models.CharField(max_length=20, help_text="Telefone Ex: (61) 91234-5678")

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="disponivel",
        help_text="Status do motorista",
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora do cadastro do motorista"
    )

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    motorista = models.OneToOneField(
        "Motorista",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veiculo",
    )


class Rota(models.Model):
    motorista = models.ForeignKey(
        Motorista, on_delete=models.PROTECT, related_name="rotas"
    )
    nome = models.CharField(max_length=100)


class Entrega(models.Model):
    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
    )
    codigo_rastreio = models.CharField(max_length=50)
