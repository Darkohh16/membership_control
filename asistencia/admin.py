from django.contrib import admin
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('socio', 'fecha_hora', 'metodo_registro')
    list_filter = ('metodo_registro', 'fecha_hora')
    search_fields = ('socio__username', 'socio__first_name', 'socio__last_name')
    date_hierarchy = 'fecha_hora'
