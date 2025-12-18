from rest_framework import permissions
from .models import Motorista


class IsGestor(permissions.BasePermission):
    """
    Permite acesso total apenas aos gestores (usuários com is_staff=True).
    Conforme requisito: Gestores possuem CRUD completo em todas as entidades.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class IsMotorista(permissions.BasePermission):
    """
    Permissão personalizada para Motoristas.
    - Leitura/Escrita: Apenas em dados próprios (rotas ou entregas atribuídas).
    - Restrição: Não podem deletar registros (histórico deve ser mantido).
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if not hasattr(request.user, "motorista") or request.method == "DELETE":
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        # Motorista pode acessar seu próprio registro de Motorista
        if isinstance(obj, Motorista) and obj == request.user.motorista:
            return True

        if getattr(obj, "motorista", None) == request.user.motorista:
            return True

        if getattr(obj, "rota", None) and obj.rota.motorista == request.user.motorista:
            return True

        return False


class IsCliente(permissions.BasePermission):
    """
    Permissão personalizada para Clientes.
    - Acesso somente leitura (GET, HEAD, OPTIONS).
    - Acesso restrito apenas aos seus próprios dados.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if request.method not in permissions.SAFE_METHODS:
            return False

        if not hasattr(request.user, "cliente"):
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if hasattr(obj, "cliente"):
            return obj.cliente == request.user.cliente

        return False
