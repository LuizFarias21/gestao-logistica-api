from django.contrib import admin
from .models import Motorista

class MotoristaAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de motoristas no painel de administração
    list_display = ('nome', 'cpf', 'cnh', 'status', 'veiculo_atual_id', 'data_cadastro')
    
    # Adiciona a capacidade de pesquisar motoristas pelo nome e documentos
    search_fields = ('nome', 'cpf', 'cnh')
    
    # Permite filtrar a lista por status (ex: listar apenas 'disponíveis')
    list_filter = ('status',)
    
    # Define a ordem padrão (ex: ordenar pelo nome)
    ordering = ('nome',)

    # Campos que não podem ser editados após o cadastro (ex: data de cadastro)
    readonly_fields = ('data_cadastro',) 
    
    # Agrupamento e layout dos campos no formulário de edição/criação
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'cpf', 'cnh', 'telefone')
        }),
        ('Status e Logística', {
            'fields': ('status', 'veiculo_atual_id', 'data_cadastro')
        }),
    )

# 1. Registra o modelo Motorista no painel de administração do Django
admin.site.register(Motorista, MotoristaAdmin)
