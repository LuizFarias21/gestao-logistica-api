from django.contrib import admin
from .models import Cliente, Motorista, Rota, Veiculo, Entrega

try:
    from django.contrib.admin.sites import AlreadyRegistered
    from rest_framework.authtoken.admin import TokenAdmin
    from rest_framework.authtoken.models import Token

    try:
        admin.site.register(Token, TokenAdmin)
    except AlreadyRegistered:
        pass
except Exception:
    # Se o app authtoken não estiver instalado por algum motivo, não quebra o admin.
    pass


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "user")
    search_fields = ("nome", "telefone", "user__username", "user__email")
    ordering = ("id",)
    autocomplete_fields = ("user",)


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "cpf", "status", "telefone", "user", "data_cadastro")
    search_fields = ("nome", "cpf", "cnh", "telefone", "user__username", "user__email")
    list_filter = ("status", "data_cadastro")
    ordering = ("-data_cadastro", "id")
    date_hierarchy = "data_cadastro"
    readonly_fields = ("data_cadastro",)
    autocomplete_fields = ("user",)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "placa",
        "modelo",
        "tipo",
        "status",
        "capacidade_maxima",
        "km_atual",
        "motorista",
    )
    search_fields = ("placa", "modelo", "motorista__nome", "motorista__cpf")
    list_filter = ("tipo", "status")
    ordering = ("placa",)
    autocomplete_fields = ("motorista",)
    list_select_related = ("motorista",)


@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "status", "motorista", "veiculo", "data_rota")
    search_fields = (
        "nome",
        "descricao",
        "motorista__nome",
        "motorista__cpf",
        "veiculo__placa",
    )
    list_filter = ("status", "data_rota")
    ordering = ("-data_rota", "id")
    date_hierarchy = "data_rota"
    readonly_fields = ("data_rota",)
    autocomplete_fields = ("motorista", "veiculo")
    list_select_related = ("motorista", "veiculo")


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "codigo_rastreio",
        "status",
        "cliente",
        "motorista",
        "rota",
        "capacidade_necessaria",
        "valor_frete",
        "data_solicitacao",
        "data_entrega_prevista",
        "data_entrega_real",
    )
    search_fields = (
        "codigo_rastreio",
        "cliente__nome",
        "cliente__user__username",
        "motorista__nome",
        "motorista__cpf",
        "rota__nome",
        "endereco_origem",
        "endereco_destino",
    )
    list_filter = (
        "status",
        "data_solicitacao",
        "data_entrega_prevista",
        "data_entrega_real",
    )
    ordering = ("-data_solicitacao", "id")
    date_hierarchy = "data_solicitacao"
    readonly_fields = ("data_solicitacao",)
    autocomplete_fields = ("cliente", "motorista", "rota")
    list_select_related = ("cliente", "motorista", "rota")
