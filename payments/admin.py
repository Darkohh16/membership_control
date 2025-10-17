from django.contrib import admin
from payments.models import Pago


# Register your models here.
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Pago.
    """
    list_display = (
        'numero_recibo',
        'usuario',
        'monto',
        'metodo_pago',
        'estado',
        'fecha_pago',
        'registrado_por'
    )
    
    list_filter = (
        'estado',
        'metodo_pago',
        'fecha_pago',
    )
    
    search_fields = (
        'numero_recibo',
        'usuario__username',
        'usuario__email',
        'concepto',
    )
    
    readonly_fields = (
        'numero_recibo',
        'fecha_creacion',
        'fecha_actualizacion',
    )
    
    fieldsets = (
        ('Información del Pago', {
            'fields': (
                'numero_recibo',
                'usuario',
                'monto',
                'metodo_pago',
                'estado',
            )
        }),
        ('Detalles Adicionales', {
            'fields': (
                'concepto',
                'notas',
                'registrado_por',
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_pago',
                'fecha_creacion',
                'fecha_actualizacion',
            ),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'fecha_pago'
    ordering = ('-fecha_pago',)
    
    def save_model(self, request, obj, form, change):
        """
        Registra automáticamente quién está creando/editando el pago.
        """
        if not change:  # Si es un nuevo registro
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
