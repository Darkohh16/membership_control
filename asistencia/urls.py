from django.urls import path 
from . import views 

app_name = 'asistencia' 

urlpatterns = [
    path('', views.historial_asistencia, name='historial'),  # Vista principal
    path('buscar/', views.buscar_socio, name='buscar_socio'),
    path('registrar/<uuid:socio_id>/', views.registrar_asistencia_directo, name='registrar_asistencia_directo'),
]