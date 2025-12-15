from django.db import models
from django.core.exceptions import ValidationError


class Motorista(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = "disponivel", "Disponivel"
        EM_ROTA = "em_rota", "Em rota"

    nome = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DISPONIVEL,
    )

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    capacidade_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.placa


class Entrega(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_TRANSITO = "em_transito", "Em transito"
        ENTREGUE = "entregue", "Entregue"

    descricao = models.CharField(max_length=255)
    capacidade = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    def __str__(self):
        return self.descricao


class Rota(models.Model):
    class Status(models.TextChoices):
        PLANEJADO = "planejado", "Planejado"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDO = "concluido", "Concluido"

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.PROTECT,
        related_name="rotas",
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="rotas",
    )

    entregas = models.ManyToManyField(
        Entrega,
        related_name="rotas",
        blank=True,
    )

    data_rota = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANEJADO,
    )

    capacidade_total_utilizada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    km_total_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    tempo_estimado = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    def clean(self):
        # Veículo não pode estar em duas rotas em andamento
        if (
            self.status == self.Status.EM_ANDAMENTO
            and Rota.objects.filter(
                veiculo=self.veiculo,
                status=self.Status.EM_ANDAMENTO,
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                "Este veículo já está em uma rota em andamento."
            )

        # Motorista precisa estar disponível
        if (
            self.status == self.Status.EM_ANDAMENTO
            and self.motorista.status != Motorista.Status.DISPONIVEL
        ):
            raise ValidationError(
                "O motorista não está disponível para iniciar a rota."
            )

    def __str__(self):
        return f"{self.nome} ({self.get_status_display()})"
