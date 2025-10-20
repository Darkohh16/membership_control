from django.urls import path 
from . import views 

app_name = 'asistencia' 

urlpatterns = [
    path('registrar-form/', views.registrar_asistencia_form, name='registrar_asistencia_form'),
    path('historial/', views.historial_asistencia, name='historial'),
    path('buscar/', views.buscar_socio, name='buscar_socio'),  # ← AGREGAR
    path('registrar/<str:socio_username>/', views.registrar_asistencia_directo, name='registrar_asistencia_directo'),
]