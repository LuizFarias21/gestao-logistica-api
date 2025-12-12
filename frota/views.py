from rest_framework import generics
from .models import Veiculo
from .serializers import VeiculoSerializer


class VeiculoCreateView(generics.CreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer


class VeiculoListView(generics.ListAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer


class VeiculoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
