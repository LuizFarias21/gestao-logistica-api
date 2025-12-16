from django.contrib import admin
from .models import Cliente, Motorista, Rota, Veiculo, Entrega


@admin.register(Cliente)
class ClienteAdmin(admin.site.ModelAdmin):
    # TODO: Configurar ClienteAdmin
    pass


@admin.register(Motorista)
class MotoristaAdmin(admin.site.ModelAdmin):
    # TODO: Configurar MotoristaAdmin
    pass


@admin.register(Veiculo)
class VeiculoAdmin(admin.site.ModelAdmin):
    # TODO: Configurar VeiculoAdmin
    pass


@admin.register(Rota)
class RotaAdmin(admin.site.ModelAdmin):
    # TODO: Configurar RotaAdmin
    pass


@admin.register(Entrega)
class EntregaAdmin(admin.site.ModelAdmin):
    # TODO: Configurar EntregaAdmin
    pass
