from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Cliente, Motorista, Veiculo, Rota, Entrega
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

   
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsGestor]

    @action(detail=True, methods=["patch"], url_path="atribuir-veiculo", permission_classes=[IsGestor])
    def atribuir_veiculo(self, request, pk=None):
        motorista = self.get_object()
        veiculo_id = request.data.get("veiculo_id")

      
        if veiculo_id is None:
            try:
                veiculo_atual = motorista.veiculo
            except Veiculo.DoesNotExist:
                veiculo_atual = None

            if veiculo_atual:
                veiculo_atual.motorista = None
                veiculo_atual.save()

            motorista.status = "disponivel"
            motorista.save()

            serializer = MotoristaSerializer(motorista)
            return Response({"detail": "Veículo desvinculado com sucesso.", "motorista": serializer.data})

   
        try:
            veiculo_id = int(veiculo_id)
        except (TypeError, ValueError):
            return Response({"detail": "O 'veiculo_id' deve ser um número inteiro."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            veiculo = Veiculo.objects.get(pk=veiculo_id)
        except Veiculo.DoesNotExist:
            return Response({"detail": "Veículo não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        
        if veiculo.motorista and veiculo.motorista != motorista:
            return Response({"detail": f"Veículo de ID {veiculo_id} já está em uso por outro motorista."}, status=status.HTTP_409_CONFLICT)

      
        veiculo.motorista = motorista
        veiculo.save()

        motorista.status = "disponivel"
        motorista.save()

        serializer = MotoristaSerializer(motorista)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="entregas", permission_classes=[IsMotorista])
    def entregas(self, request, pk=None):
        motorista = self.get_object()

       
        if not request.user.is_staff:
            if not hasattr(request.user, "motorista") or request.user.motorista.id != motorista.id:
                return Response({"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN)

        entregas = Entrega.objects.filter(motorista=motorista)
        serializer = EntregaSerializer(entregas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="rotas", permission_classes=[IsMotorista])
    def rotas(self, request, pk=None):
        motorista = self.get_object()

        if not request.user.is_staff:
            if not hasattr(request.user, "motorista") or request.user.motorista.id != motorista.id:
                return Response({"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN)

        rotas = Rota.objects.filter(motorista=motorista)
        serializer = RotaSerializer(rotas, many=True)
        return Response(serializer.data)

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
