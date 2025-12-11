from django.db import models


class Motorista(models.Model):
    nome = models.CharField(max_length=100)


class Veiculo(models.Model):
    TIPO_VEICULOS = (
        ("CARRO", "Carro"),
        ("VAN", "Van"),
        ("CAMINHAO", "Caminhão"),
    )

    STATUS_VEICULOS = (
        ("DISPONIVEL", "Disponível"),
        ("EM_USO", "Em uso"),
        ("MANUTENCAO", "Manutenção"),
    )

    placa = models.CharField(
        max_length=7, unique=True, help_text="Placa sem traços (EX: ABC1234)"
    )

    modelo = models.CharField(
        max_length=70, help_text="Modelo e Marca (Ex: Fiat Ducato)"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_VEICULOS,
        default="CARRO",
        help_text="Tipo de veículo",
    )

    capacidade_maxima = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Capacidade em KG"
    )

    km_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Leitura atual do hodômetro em KM",
    )

    status = models.CharField(
        max_length=20, choices=STATUS_VEICULOS, default="DISPONIVEL"
    )

    motorista = models.OneToOneField(
        "Motorista",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veiculo_atual",
        help_text="Motorista responsável pelo veículo no momento",
    )

    def __str__(self):
        return f"{self.modelo} ({self.placa})"
