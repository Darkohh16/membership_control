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
        'socio',
        'get_membresia_display',
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
        'socio__nombre',
        'socio__apellido',
        'socio__dni_carnet',
        'socio__correo',
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
                'socio',
                'membresia',
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
    
    def get_membresia_display(self, obj):
        """
        Muestra la membresía asociada al pago.
        """
        if obj.membresia:
            return f"{obj.membresia.tipo_membresia.nombre}"
        return "-"
    get_membresia_display.short_description = 'Membresía'
    
    def save_model(self, request, obj, form, change):
        """
        Registra automáticamente quién está creando/editando el pago.
        """
        if not change:  # Si es un nuevo registro
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
