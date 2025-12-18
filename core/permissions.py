from rest_framework import permissions


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
    - Leitura (GET): Permitida.
    - Escrita (PUT/PATCH): Permitida para atualizar status ou observações.
    - Criação (POST): Negada (Motoristas não criam entregas ou rotas).
    - Exclusão (DELETE): Negada (Histórico deve ser mantido).
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if not hasattr(request.user, "motorista"):
            return False

        if request.method in ["POST", "DELETE"]:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        motorista = request.user.motorista

        if obj == motorista:
            return True

        if getattr(obj, "motorista", None) == motorista:
            return True

        rota = getattr(obj, "rota", None)
        if rota and getattr(rota, "motorista", None) == motorista:
            return True

        return False


class IsCliente(permissions.BasePermission):
    """
    Permissão personalizada para Clientes.
    - Acesso Somente-Leitura (GET, HEAD, OPTIONS).
    - Não podem criar, editar ou deletar nada.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if not hasattr(request.user, "cliente"):
            return False

        if request.method not in permissions.SAFE_METHODS:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if hasattr(obj, "cliente") and obj.cliente == request.user.cliente:
            return True

        if obj == request.user.cliente:
            return True

        return False
