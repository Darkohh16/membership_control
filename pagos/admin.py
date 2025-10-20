from django.contrib import admin
from .models import TipoMembresia, Socio, Pago

@admin.register(TipoMembresia)
class TipoMembresiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_dias', 'precio')
    search_fields = ('nombre',)

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'tipo_membresia', 'fecha_inicio', 'fecha_fin', 'estado')
    search_fields = ('nombre', 'dni', 'correo')
    list_filter = ('estado', 'tipo_membresia')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('socio', 'fecha_pago', 'monto', 'metodo_pago')
    list_filter = ('metodo_pago', 'fecha_pago')
    search_fields = ('socio__nombre', 'socio__dni')
