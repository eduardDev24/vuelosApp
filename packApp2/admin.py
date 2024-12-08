
from django.contrib import admin, messages

from packApp2.models import Pack_promocion
from vueloApp.models import Boleto

# Register your models here.


class PackPromocionAdmin(admin.ModelAdmin):
    list_display = ('destino', 'estadias', 'transporte',
                    'comidas', 'hoteles', 'precio', 'nombre')

    def delete_model(self, request, obj):
        # Verificar si el pack está asociado a algún boleto
        if Boleto.objects.filter(pack=obj).exists():
            # Si hay boletos asociados, mostrar un mensaje de advertencia
            messages.warning(
                request,
                f"No se puede eliminar el Pack '{
                    obj.nombre}' porque está asociado a uno o más boletos."
            )
        else:
            # Si no hay boletos asociados, proceder con la eliminación
            super().delete_model(request, obj)
            messages.success(
                request,
                f"El Pack '{obj.nombre}' se eliminó correctamente."
            )

    def delete_queryset(self, request, queryset):
        # Creamos una lista para packs no eliminables
        non_deletable_packs = []
        deletions_count = 0  # Contador de eliminaciones realizadas

        # Recorrer cada pack en la selección
        for obj in queryset:
            if Boleto.objects.filter(pack=obj).exists():
                # Si el pack está asociado a boletos, no lo eliminamos
                non_deletable_packs.append(obj.nombre)
            else:
                # Si no está asociado, lo eliminamos
                obj.delete()
                deletions_count += 1

        # Mostrar un mensaje de advertencia si hay packs no eliminables
        if non_deletable_packs:
            messages.warning(
                request,
                f"No se pueden eliminar los siguientes packs porque están asociados a boletos: {
                    ', '.join(non_deletable_packs)}."
            )

        # Mostrar mensaje de éxito solo si se eliminaron packs
        if deletions_count > 0:
            messages.success(
                request,
                f"Se eliminaron correctamente {deletions_count} pack(s)."
            )
        else:
            # Si no se eliminaron packs, no mostramos el mensaje de éxito
            messages.info(
                request,
                "No se eliminaron packs porque todos están asociados a boletos."

            )


admin.site.register(Pack_promocion, PackPromocionAdmin)
