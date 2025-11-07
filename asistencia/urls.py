from django.urls import path 
from . import views 

app_name = 'asistencia' 

urlpatterns = [
    path('registrar-form/', views.registrar_asistencia_form, name='registrar_asistencia_form'),
    path('historial/', views.historial_asistencia, name='historial'),
    path('buscar/', views.buscar_socio, name='buscar_socio'),
    # Cambio importante: ahora usa UUID en vez de username
    path('registrar/<uuid:socio_id>/', views.registrar_asistencia_directo, name='registrar_asistencia_directo'),
]