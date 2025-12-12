from django.db import models
from django.conf import settings


class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("ativo", "Ativo"),
            ("manutencao", "Em Manutenção"),
            ("inativo", "Inativo"),
        ],
        default="ativo",
    )

    # relação 1:1 com motorista
    motorista = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veiculo_atual",
    )

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
