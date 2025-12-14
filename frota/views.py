from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Motorista
from .serializers import MotoristaSerializer


# --- 1. ViewSet para CRUD Básico (Acesso Exclusivo Gestor) ---
class MotoristaViewSet(viewsets.ModelViewSet):
    """
    Endpoints: GET /api/motoristas/, POST, GET/PUT/DELETE /api/motoristas/{id}/
    """
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer

    # Sobrescreve o método de exclusão para aplicar a Regra de Negócio
    def destroy(self, request, *args, **kwargs):
        motorista = self.get_object()
        
        # Regra de Negócio: Impede a exclusão se o status for 'em_rota'
        if motorista.status == 'em_rota':
            return Response(
                {"detail": "Não é possível excluir motorista com status 'em_rota'.", "status_code": 403},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)


# --- 2. Rota Customizada para Atribuir Veículo (PATCH) ---
class AtribuirVeiculoAPIView(APIView):
    """
    Endpoint: PATCH /api/motoristas/{id}/atribuir-veiculo/
    Implementa o vínculo 1:1.
    """
    def patch(self, request, motorista_id):
        motorista = get_object_or_404(Motorista, pk=motorista_id)
        veiculo_id = request.data.get('veiculo_id')

        # Permite desvincular o veículo (ex: enviar {"veiculo_id": null})
        if veiculo_id is None:
            motorista.veiculo_atual_id = None
            motorista.status = 'disponivel'
            motorista.save()
            return Response({"detail": "Veículo desvinculado com sucesso."}, status=status.HTTP_200_OK)

        # Validação do ID
        try:
            veiculo_id = int(veiculo_id)
        except (TypeError, ValueError):
             return Response({"detail": "O 'veiculo_id' deve ser um número inteiro."}, status=status.HTTP_400_BAD_REQUEST)


        # Critério de Aceite: Impede que um veículo já em uso seja selecionado
        # Verifica se o veículo JÁ está atribuído a OUTRO motorista.
        if Motorista.objects.exclude(pk=motorista_id).filter(veiculo_atual_id=veiculo_id).exists():
            return Response(
                {"detail": f"Veículo de ID {veiculo_id} já está em uso por outro motorista (regra 1:1)."},
                status=status.HTTP_409_CONFLICT
            )

        # Vincula o novo veículo e atualiza o status
        motorista.veiculo_atual_id = veiculo_id
        motorista.status = 'disponivel' 
        motorista.save()

        serializer = MotoristaSerializer(motorista)
        return Response(serializer.data, status=status.HTTP_200_OK)