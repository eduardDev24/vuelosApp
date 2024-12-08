from rest_framework.permissions import BasePermission


class UsuarioAdministrador(BasePermission):

    def tiene_permiso(self, request, view):
        # Permite el acceso solo si el usuario está autenticado y es administrador
        return request.user.is_authenticated and request.user.is_staff
