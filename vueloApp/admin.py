from django.contrib import admin


from django.contrib import admin
from .models import Pais, Aerolinea, Asiento, Horario, Boleto, Contacto

# Clase para administrar el modelo Pais
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Clase para administrar el modelo Aerolinea
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo','descripcion')
    search_fields = ('nombre', 'codigo', 'descripcion')

# Clase para administrar el modelo Asiento
class AsientoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'disponible', 'precio')
    list_filter = ('numero','disponible', 'precio')

# Clase para administrar el modelo Horario
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('hora_salida', 'hora_llegada')

# Clase para administrar el modelo Boleto
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'destino_ida', 'destino_vuelta', 'asiento', 'horario', 'aerolinea', 'total_viaje')
    list_filter = ('destino_ida', 'destino_vuelta', 'aerolinea')
    search_fields = ('nombre', 'rut')

# Clase para administrar el modelo Contacto
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'mensaje', 'fecha')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha',)

# Registrar los modelos con sus respectivas clases de administración
admin.site.register(Pais, PaisAdmin)
admin.site.register(Aerolinea, AerolineaAdmin)
admin.site.register(Asiento, AsientoAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Boleto, BoletoAdmin)
admin.site.register(Contacto, ContactoAdmin)
