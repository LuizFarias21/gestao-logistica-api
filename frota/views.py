# frota/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Motorista # Garanta que você importou o modelo correto
from .serializers import MotoristaSerializer


# --- 1. ViewSet para CRUD Básico (Acesso Exclusivo Gestor) ---
class MotoristaViewSet(viewsets.ModelViewSet):
    """
    Lida com Listar (/api/motoristas/), Criar, Detalhar, Atualizar e Deletar motoristas.
    """
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer

    # Sobrescreve o método de exclusão para aplicar a Regra de Negócio
    def destroy(self, request, *args, **kwargs):
        motorista = self.get_object()
        
        # Regra de Negócio (4. Status): Impede a exclusão se o status for 'em_rota'
        if motorista.status == 'em_rota':
            return Response(
                {"detail": "Não é possível excluir motorista com status 'em_rota'.", "status_code": 403},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Se não estiver em rota, permite o delete
        return super().destroy(request, *args, **kwargs)


# --- 2. Rota Customizada para Atribuir Veículo (PATCH) ---
class AtribuirVeiculoAPIView(APIView):
    """
    Endpoint: PATCH /api/motoristas/{id}/atribuir-veiculo/
    Implementa o vínculo 1:1 e garante que o veículo não está em uso.
    """
    def patch(self, request, motorista_id):
        # 1. Busca o motorista
        motorista = get_object_or_404(Motorista, pk=motorista_id)
        veiculo_id = request.data.get('veiculo_id')

        if veiculo_id is None:
            # Caso o usuário queira desvincular o veículo (ex: enviar {"veiculo_id": null})
            motorista.veiculo_atual_id = None
            motorista.status = 'disponivel'
            motorista.save()
            return Response({"detail": "Veículo desvinculado com sucesso.", "status_code": 200}, status=status.HTTP_200_OK)

        try:
            veiculo_id = int(veiculo_id)
        except ValueError:
             return Response({"detail": "O 'veiculo_id' deve ser um número inteiro ou nulo.", "status_code": 400}, status=status.HTTP_400_BAD_REQUEST)


        # 2. Critério de Aceite: Impede que um veículo já em uso seja selecionado
        # Verifica se o veículo JÁ está atribuído a OUTRO motorista (excluindo o motorista atual)
        if Motorista.objects.exclude(pk=motorista_id).filter(veiculo_atual_id=veiculo_id).exists():
            return Response(
                {"detail": f"Veículo de ID {veiculo_id} já está em uso por outro motorista (regra 1:1).", "status_code": 409},
                status=status.HTTP_409_CONFLICT
            )

        # 3. Vincula o novo veículo e atualiza o status
        motorista.veiculo_atual_id = veiculo_id
        # Regra de Negócio: Ao vincular um veículo, o status do motorista deve mudar para "disponível/em_rota"
        motorista.status = 'disponivel' # Mudando para 'disponivel' por convenção
        motorista.save()

        # Retorna o motorista atualizado
        serializer = MotoristaSerializer(motorista)
        return Response(serializer.data, status=status.HTTP_200_OK)

