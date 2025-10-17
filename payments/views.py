from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

from payments.models import Pago
from payments.constants import METODOS_PAGO, ESTADOS_PAGO

# Create your views here.

@login_required
def listar_pagos(request):
    """
    Vista para listar todos los pagos con filtros opcionales.
    """
    pagos = Pago.objects.all()
    
    # Filtros
    estado_filtro = request.GET.get('estado')
    metodo_filtro = request.GET.get('metodo')
    buscar = request.GET.get('q')
    
    if estado_filtro:
        pagos = pagos.filter(estado=estado_filtro)
    
    if metodo_filtro:
        pagos = pagos.filter(metodo_pago=metodo_filtro)
    
    if buscar:
        pagos = pagos.filter(
            Q(numero_recibo__icontains=buscar) |
            Q(usuario__username__icontains=buscar) |
            Q(concepto__icontains=buscar)
        )
    
    context = {
        'pagos': pagos,
        'metodos_pago': METODOS_PAGO,
        'estados_pago': ESTADOS_PAGO,
    }
    
    return render(request, 'payments/listar_pagos.html', context)


@login_required
def detalle_pago(request, pago_id):
    """
    Vista para ver el detalle de un pago específico.
    """
    pago = get_object_or_404(Pago, pk=pago_id)
    
    context = {
        'pago': pago,
    }
    
    return render(request, 'payments/detalle_pago.html', context)


@login_required
def registrar_pago(request):
    """
    Vista para registrar un nuevo pago.
    Solo accesible para administradores.
    """
    # Verificar que el usuario sea administrador
    if request.user.perfil != 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('listar_pagos')
    
    if request.method == 'POST':
        # Aquí iría la lógica para crear el pago
        # Por ahora solo mostramos el formulario
        messages.success(request, 'Pago registrado exitosamente.')
        return redirect('listar_pagos')
    
    context = {
        'metodos_pago': METODOS_PAGO,
        'estados_pago': ESTADOS_PAGO,
    }
    
    return render(request, 'payments/registrar_pago.html', context)


@login_required
def mis_pagos(request):
    """
    Vista para que un usuario vea sus propios pagos.
    """
    pagos = Pago.objects.filter(usuario=request.user)
    
    context = {
        'pagos': pagos,
    }
    
    return render(request, 'payments/mis_pagos.html', context)


@login_required
def reporte_pagos(request):
    """
    Vista para generar reportes de pagos.
    Solo accesible para administradores.
    """
    if request.user.perfil != 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('listar_pagos')
    
    # Obtener estadísticas
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    
    pagos_mes = Pago.objects.pagos_del_mes(mes_actual, anio_actual)
    total_recaudado = Pago.objects.total_recaudado()
    pagos_por_metodo = Pago.objects.pagos_por_metodo()
    
    context = {
        'pagos_mes': pagos_mes,
        'total_recaudado': total_recaudado,
        'pagos_por_metodo': pagos_por_metodo,
    }
    
    return render(request, 'payments/reporte_pagos.html', context)