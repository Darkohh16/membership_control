from django.urls import path
from membresias import views

urlpatterns = [
    path('tipos/', views.listar_tipos, name='listar_tipos'),
    path('tipos/crear/', views.crear_tipo, name='crear_tipo'),
    path('tipos/editar/<int:tipo_id>/', views.editar_tipo, name='editar_tipo'),
    path('asignar/', views.asignar_membresia, name='asignar_membresia'),
    path('socio/<uuid:socio_id>/', views.listar_membresias_socio, name='listar_membresias_socio'),
    path('desactivar/<int:membresia_id>/', views.desactivar_membresia, name='desactivar_membresia'),
    # API endpoints - UUID para socios
    path('api/socio/<uuid:socio_id>/', views.api_membresias_socio, name='api_membresias_socio'),
]