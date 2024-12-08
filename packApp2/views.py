from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from packApp2.models import Pack_promocion
from django.contrib.auth.decorators import login_required
from packApp2.permission import UsuarioAdministrador
from packApp2.serializer import PackPromocionSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated


@login_required(login_url='login')
def pack_promocion(request):
    # Recupera todos los packs de promociones
    promociones = Pack_promocion.objects.all()
    # Obtén el ID de promoción si está en la URL
    promocion_id = request.GET.get('id')
    # Si hay un ID de promoción, recupera esa promoción específica
    if promocion_id:
        promocion = Pack_promocion.objects.filter(id=promocion_id).first()
        if promocion:
            return render(request, 'ver_seleccion.html', {'promocion': promocion})
    # Si no hay ID, muestra todas las promociones
    return render(request, 'pack_promocion.html', {'promociones': promociones})


@login_required(login_url='login')
def ver_seleccion(request, id):
    # Obtener la promoción seleccionada, o un error 404 si no existe
    promocion = get_object_or_404(Pack_promocion, id=id)

    # Renderizar el template con los datos de la promoción
    return render(request, 'ver_seleccion.html', {'promocion': promocion})


# Rest_framework apiRest
class PackPromocionViewSets(viewsets.ModelViewSet):
    queryset = Pack_promocion.objects.all()
    serializer_class = PackPromocionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        # Restringir acceso al CRUD solo a administradores autenticados
        if self.request.method in ['GET', 'POST', 'PUT', 'DELETE']:
            return [IsAdminUser(), UsuarioAdministrador()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response({"error": "No tienes permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
