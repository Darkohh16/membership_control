from django.contrib import admin
from .models import Asistencia
from accounts.models import Usuario

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('socio', 'fecha_hora')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "socio":
            kwargs["queryset"] = Usuario.objects.filter(perfil=2)  # solo usuarios/socios
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
