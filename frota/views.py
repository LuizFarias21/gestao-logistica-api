from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Motorista

# Create your views here.

class MotoristaListView(ListView):
    model = Motorista
    template_name = 'frota/motorista_list.html'
    context_object_name = 'motoristas'
    paginate_by = 20
    ordering = ['nome']

class MotoristaDetailView(DetailView):
    model = Motorista
    template_name = 'frota/motorista_detail.html'
    context_object_name = 'motorista'

class MotoristaCreateView(CreateView):
    model = Motorista
    fields = ['nome', 'cpf', 'cnh', 'telefone', 'status']
    template_name = 'frota/motorista_form.html'
    success_url = reverse_lazy('frota:motorista_list')

class MotoristaUpdateView(UpdateView):
    model = Motorista
    fields = ['nome', 'cpf', 'cnh', 'telefone', 'status']
    template_name = 'frota/motorista_form.html'
    success_url = reverse_lazy('frota:motorista_list')

class MotoristaDeleteView(DeleteView):
    model = Motorista
    template_name = 'frota/motorista_confirm_delete.html'
    success_url = reverse_lazy('frota:motorista_list')
