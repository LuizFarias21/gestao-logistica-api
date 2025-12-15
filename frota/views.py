from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Motorista
from .serializers import MotoristaSerializer
from rest_framework.exceptions import ValidationError
from logistica.models import Entrega
from logistica.serializers import EntregaSerializer


class MotoristaViewSet(viewsets.ModelViewSet):
    """
    Endpoints: GET /api/motoristas/, POST, GET/PUT/DELETE /api/motoristas/{id}/
    """

    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer

    def perform_destroy(self, instance):
        if instance.status == "em_rota":
            raise ValidationError(
                {
                    "erro:": "Não é possível excluir um motorista que está em rota. Finalize a rota primeiro."
                }
            )

        instance.delete()


class AtribuirVeiculoAPIView(APIView):
    """
    Endpoint: PATCH /api/motoristas/{id}/atribuir-veiculo/
    Implementa o vínculo 1:1.
    """

    def patch(self, request, motorista_id):
        motorista = get_object_or_404(Motorista, pk=motorista_id)
        veiculo_id = request.data.get("veiculo_id")

        if veiculo_id is None:
            motorista.veiculo_atual_id = None
            motorista.status = "disponivel"
            motorista.save()
            return Response(
                {"detail": "Veículo desvinculado com sucesso."},
                status=status.HTTP_200_OK,
            )

        try:
            veiculo_id = int(veiculo_id)
        except (TypeError, ValueError):
            return Response(
                {"detail": "O 'veiculo_id' deve ser um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            Motorista.objects.exclude(pk=motorista_id)
            .filter(veiculo_atual_id=veiculo_id)
            .exists()
        ):
            return Response(
                {
                    "detail": f"Veículo de ID {veiculo_id} já está em uso por outro motorista (regra 1:1)."
                },
                status=status.HTTP_409_CONFLICT,
            )

        motorista.veiculo_atual_id = veiculo_id
        motorista.status = "disponivel"
        motorista.save()

        serializer = MotoristaSerializer(motorista)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MotoristaEntregasView(APIView):
    def get(self, request, id):
        motorista = get_object_or_404(Motorista, id=id)

        entregas = Entrega.objects.filter(motorista=motorista)

        serializer = EntregaSerializer(entregas, many=True)
        return Response(serializer.data)
