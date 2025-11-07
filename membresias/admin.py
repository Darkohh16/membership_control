from django.contrib import admin
from membresias.models import TipoMembresia, Membresia


@admin.register(TipoMembresia)
class TipoMembresiaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para TipoMembresia.
    """
    list_display = (
        'nombre',
        'duracion_dias',
        'precio',
        'activo',
        'fecha_creacion'
    )
    
    list_filter = (
        'activo',
        'duracion_dias',
        'fecha_creacion',
    )
    
    search_fields = (
        'nombre',
        'descripcion',
    )
    
    readonly_fields = (
        'fecha_creacion',
        'fecha_actualizacion',
    )
    
    fieldsets = (
        ('Información del Tipo', {
            'fields': (
                'nombre',
                'duracion_dias',
                'precio',
                'activo',
            )
        }),
        ('Detalles', {
            'fields': (
                'descripcion',
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_creacion',
                'fecha_actualizacion',
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('precio', 'duracion_dias')


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Membresia.
    """
    list_display = (
        'socio',
        'tipo_membresia',
        'fecha_inicio',
        'fecha_fin',
        'activa',
        'pagada',
        'dias_restantes_display',
    )
    
    list_filter = (
        'activa',
        'pagada',
        'tipo_membresia',
        'fecha_inicio',
        'fecha_fin',
    )
    
    search_fields = (
        'socio__nombre',
        'socio__apellido',
        'socio__dni_carnet',
        'tipo_membresia__nombre',
    )
    
    readonly_fields = (
        'fecha_creacion',
        'fecha_actualizacion',
        'dias_restantes_display',
    )
    
    fieldsets = (
        ('Información de la Membresía', {
            'fields': (
                'socio',
                'tipo_membresia',
                'activa',
                'pagada',
            )
        }),
        ('Período', {
            'fields': (
                'fecha_inicio',
                'fecha_fin',
                'dias_restantes_display',
            )
        }),
        ('Observaciones', {
            'fields': (
                'observaciones',
            ),
            'classes': ('collapse',)
        }),
        ('Fechas del Sistema', {
            'fields': (
                'fecha_creacion',
                'fecha_actualizacion',
            ),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'fecha_inicio'
    ordering = ('-fecha_inicio',)
    
    def dias_restantes_display(self, obj):
        """Muestra los días restantes de forma amigable"""
        if obj.esta_vencida():
            return "❌ Vencida"
        dias = obj.dias_restantes()
        if dias == 0:
            return "⚠️ Vence hoy"
        elif dias <= 7:
            return f"⚠️ {dias} días"
        return f"✅ {dias} días"
    
    dias_restantes_display.short_description = "Estado"
