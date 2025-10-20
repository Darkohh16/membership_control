from django.urls import path
from . import views

urlpatterns = [
    path('historial/<int:socio_id>/', views.historial_pagos, name='historial_pagos'),
]
