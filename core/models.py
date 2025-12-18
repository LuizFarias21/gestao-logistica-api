from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")

    nome = models.CharField(max_length=120, help_text="Nome completo ou Razão Social")

    endereco = models.CharField(max_length=255, help_text="Endereço principal")

    telefone = models.CharField(max_length=20, help_text="Telefone para contato")

    def __str__(self):
        return f"{self.nome} ({self.user.username})"


class Motorista(models.Model):
    STATUS_CHOICES = (
        ("disponivel", "Disponível"),
        ("em_rota", "Em Rota"),
        ("inativo", "Inativo"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="motorista",
        help_text="Usuário de login associado a este perfil de cliente",
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
        max_digits=10, decimal_places=2, help_text="Capacidade em KG (EX: 320.00)"
    )

    km_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Leitura atual do hodômetro em KM",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_VEICULOS,
        default="DISPONIVEL",
        help_text="Status atual do veículo",
    )

    motorista = models.OneToOneField(
        "Motorista",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veiculo",
        help_text="Motorista responsável pelo veículo no momento",
    )

    def __str__(self):
        return f"{self.modelo} ({self.placa})"


class Rota(models.Model):
    motorista = models.ForeignKey(
        Motorista, on_delete=models.PROTECT, related_name="rotas"
    )

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name="rotas")

    nome = models.CharField(max_length=100)


class Entrega(models.Model):
    STATUS_CHOICES = (
        ("pendente", "Pendente"),
        ("em_transito", "Em Trânsito"),
        ("entregue", "Entregue"),
        ("cancelada", "Cancelada"),
    )

    codigo_rastreio = models.CharField(
        max_length=50, unique=True, help_text="Código único de rastreamento da entrega"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="entregas",
        help_text="Cliente solicitante da entrega",
    )

    rota = models.ForeignKey(
        Rota,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
        help_text="Rota associada à entrega",
    )

    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
        help_text="Motorista responsável pela entrega",
    )

    endereco_origem = models.CharField(
        max_length=255, help_text="Endereço de origem da entrega"
    )

    endereco_destino = models.CharField(
        max_length=255, help_text="Endereço de destino da entrega"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente",
        help_text="Status atual da entrega",
    )

    capacidade_necessaria = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Peso ou volume necessário em KG para o transporte",
    )

    valor_frete = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Valor do frete em reais"
    )

    data_solicitacao = models.DateTimeField(
        auto_now_add=True, null=True, help_text="Data e hora da solicitação da entrega"
    )

    data_entrega_prevista = models.DateTimeField(
        null=True, blank=True, help_text="Data e hora prevista para a entrega"
    )

    data_entrega_real = models.DateTimeField(
        null=True, blank=True, help_text="Data e hora real da entrega concluída"
    )

    observacoes = models.TextField(
        blank=True, help_text="Observações adicionais sobre a entrega"
    )

    def __str__(self):
        return f"{self.codigo_rastreio} - {self.status}"

