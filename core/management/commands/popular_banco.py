import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from core.models import Cliente, Motorista, Veiculo, Rota, Entrega

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Popula o banco de dados com dados fictícios para testes."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando a população do banco..."))

        self.criar_clientes(10)
        self.criar_motoristas_e_veiculos(5)
        self.criar_rotas_e_entregas(15)

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))

    def limpar_banco(self):
        self.stdout.write("Limpando dados antigos...")
        Entrega.objects.all().delete()
        Rota.objects.all().delete()
        Veiculo.objects.all().delete()
        Motorista.objects.all().delete()
        Cliente.objects.all().delete()

    def criar_clientes(self, qtd):
        self.stdout.write(f"Criando {qtd} clientes...")
        for _ in range(qtd):
            username = fake.user_name() + str(random.randint(1000, 9999))
            email = fake.email()

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, email=email, password="password123"
                )

                Cliente.objects.create(
                    user=user,
                    nome=fake.company(),
                    endereco=fake.address(),
                    telefone=fake.phone_number(),
                )

    def criar_motoristas_e_veiculos(self, qtd):
        self.stdout.write(f"Criando {qtd} motoristas e veículos...")
        for _ in range(qtd):
            username = fake.user_name() + str(random.randint(1000, 9999))
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, password="password123"
                )

                motorista = Motorista.objects.create(
                    user=user,
                    nome=fake.name(),
                    cpf=fake.cpf().replace(".", "").replace("-", ""),
                    cnh=str(random.randint(10000000000, 99999999999)),
                    telefone=fake.phone_number(),
                    status=random.choice(["disponivel", "em_rota", "inativo"]),
                )

                tipo = random.choice(["CARRO", "VAN", "CAMINHAO"])
                capacidade = (
                    1000.00
                    if tipo == "CAMINHAO"
                    else (500.00 if tipo == "VAN" else 200.00)
                )

                Veiculo.objects.create(
                    placa=fake.license_plate().replace("-", ""),
                    modelo=fake.vehicle_make_model()
                    if hasattr(fake, "vehicle_make_model")
                    else f"Modelo {fake.word()}",
                    tipo=tipo,
                    capacidade_maxima=capacidade,
                    km_atual=random.uniform(0, 100000),
                    status="DISPONIVEL",
                    motorista=motorista,
                )

    def criar_rotas_e_entregas(self, qtd_entregas):
        self.stdout.write("Gerando rotas e distribuindo entregas...")

        motoristas_ativos = Motorista.objects.filter(
            status__in=["disponivel", "em_rota"]
        )
        clientes = Cliente.objects.all()

        if not motoristas_ativos.exists() or not clientes.exists():
            self.stdout.write(
                self.style.ERROR("Faltam motoristas ou clientes para gerar entregas.")
            )
            return

        for motorista in motoristas_ativos:
            if hasattr(motorista, "veiculo"):
                rota = Rota.objects.create(
                    motorista=motorista,
                    veiculo=motorista.veiculo,
                    nome=f"Rota {fake.city()} - {fake.day_of_week()}",
                    descricao=fake.sentence(),
                    status="planejada",
                )

                for _ in range(random.randint(1, 5)):
                    self._criar_entrega(random.choice(clientes), rota, motorista)

        for _ in range(5):
            self._criar_entrega(random.choice(clientes), None, None)

    def _criar_entrega(self, cliente, rota, motorista):
        status_entrega = "pendente"
        data_entrega = None

        if rota:
            status_entrega = random.choice(["em_transito", "entregue"])
            if status_entrega == "entregue":
                data_entrega = timezone.now()

        Entrega.objects.create(
            codigo_rastreio=fake.uuid4()[:8].upper(),
            cliente=cliente,
            rota=rota,
            motorista=motorista,
            endereco_origem=fake.address(),
            endereco_destino=fake.address(),
            status=status_entrega,
            capacidade_necessaria=random.uniform(1.0, 50.0),
            valor_frete=random.uniform(20.0, 500.0),
            data_entrega_prevista=timezone.now()
            + timezone.timedelta(days=random.randint(1, 5)),
            data_entrega_real=data_entrega,
            observacoes=fake.text(max_nb_chars=50),
        )
