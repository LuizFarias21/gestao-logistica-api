from rest_framework import viewsets

# from drf_spectacular.utils import extend_schema
from .models import Veiculo
from .serializers import VeiculoSerializer


# @extend_schema(tags=['Frota'])
class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
