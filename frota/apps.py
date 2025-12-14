from django.apps import AppConfig


class FrotaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "frota"
    # Nome amigável que aparece no painel de administração
    verbose_name = "Gestão de Motoristas e Frota"
