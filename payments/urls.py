from django.urls import path
from payments import views

app_name = 'payments'

urlpatterns = [
    # Registrar nuevo pago (US05 - Solo administradores)
    path('registrar/', views.registrar_pago, name='registrar_pago'),
    
    # Listado y detalle de pagos
    path('', views.listar_pagos, name='listar_pagos'),
    path('<int:pago_id>/', views.detalle_pago, name='detalle_pago'),
]
