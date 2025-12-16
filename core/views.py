from rest_framework import viewsets

from .models import Cliente, Motorista, Veiculo
from .serializers import (
    ClienteSerializer,
    MotoristaSerializer,
    RotaSerializer,
    EntregaSerializer,
    VeiculoSerializer,
)
from .permissions import IsGestor, IsMotorista, IsCliente


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Clientes.
    Apenas Gestores podem cadastrar ou ver a lista de clientes.
    Clientes comuns não precisam acessar esse endpoint (eles acessam /api/entregas/).
    """

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsGestor]


class MotoristaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Motoristas (CRUD).
    Apenas Gestores podem criar, editar ou ver a lista completa de motoristas.
    """
    
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsGestor]


class VeiculoViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Veículos (CRUD).
    Apenas Gestores podem gerenciar a frota.
    """

    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsGestor]


class RotaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Rotas.
    Gestores: Acesso total.
    Motoristas: Visualizam apenas suas próprias rotas.
    """

    serializer_class = RotaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_queryset(self):
        # TODO: Implementar lógica de filtragem.
        # 1. Se for Gestor (user.is_staff) -> Retornar tudo.
        # 2. Se for Motorista -> Retornar apenas Rota.objects.filter(motorista=user.motorista)
        pass


class EntregaViewSet(viewsets.ModelViewSet):
    """
    Gerenciamento de Entregas.
    Gestores: Acesso total.
    Motoristas: Atualizam status das entregas de suas rotas.
    Clientes: Visualizam apenas suas próprias entregas (somente leitura).
    """

    serializer_class = EntregaSerializer
    permission_classes = [IsGestor | IsMotorista | IsCliente]

    def get_queryset(self):
        # TODO: Implementar lógica de filtragem de segurança.
        # 1. Gestor -> Retorna tudo.
        # 2. Motorista -> Retorna entregas vinculadas à sua rota atual.
        # 3. Cliente -> Retorna entregas vinculadas ao seu ID (user.cliente).
        pass
