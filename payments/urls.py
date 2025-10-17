from django.urls import path
from payments import views

app_name = 'payments'

urlpatterns = [
    # Listado y detalle de pagos
    path('', views.listar_pagos, name='listar_pagos'),
    path('<int:pago_id>/', views.detalle_pago, name='detalle_pago'),
    
    # Registrar nuevo pago
    path('registrar/', views.registrar_pago, name='registrar_pago'),
    
    # Mis pagos (para usuarios)
    path('mis-pagos/', views.mis_pagos, name='mis_pagos'),
    
    # Reportes (para administradores)
    path('reportes/', views.reporte_pagos, name='reporte_pagos'),
]
