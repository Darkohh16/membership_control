from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

from payments.models import Pago
from payments.constants import METODOS_PAGO, ESTADOS_PAGO
from socios.models import Socio


@login_required
def listar_pagos(request):
    """
    Vista para listar todos los pagos registrados.
    """
    pagos = Pago.objects.all().order_by('-fecha_pago')
    
    context = {
        'pagos': pagos,
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
    US05: Como administrador, quiero registrar los pagos de membresías,
    para mantener control financiero.
    """
    # Verificar que el usuario sea administrador
    if request.user.perfil != 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para registrar pagos.')
        return redirect('payments:listar_pagos')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            socio_id = request.POST.get('socio')
            monto = request.POST.get('monto')
            metodo_pago = request.POST.get('metodo_pago')
            estado = request.POST.get('estado')
            concepto = request.POST.get('concepto', '')
            notas = request.POST.get('notas', '')
            
            # Validaciones
            if not socio_id or not monto or not metodo_pago or not estado:
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('payments:registrar_pago')
            
            # Validar monto
            monto_decimal = Decimal(monto)
            if monto_decimal <= 0:
                messages.error(request, 'El monto debe ser mayor a 0.')
                return redirect('payments:registrar_pago')
            
            # Obtener el socio
            socio = Socio.objects.get(id=socio_id)
            
            # Crear el pago
            pago = Pago.objects.create(
                socio=socio,
                monto=monto_decimal,
                metodo_pago=int(metodo_pago),
                estado=int(estado),
                concepto=concepto,
                notas=notas,
                registrado_por=request.user
            )
            
            messages.success(request, f'✅ Pago registrado exitosamente. Recibo: {pago.numero_recibo}')
            return redirect('payments:detalle_pago', pago_id=pago.id)
            
        except Socio.DoesNotExist:
            messages.error(request, 'El socio seleccionado no existe.')
            return redirect('payments:registrar_pago')
        except ValueError:
            messages.error(request, 'El monto ingresado no es válido.')
            return redirect('payments:registrar_pago')
        except Exception as e:
            messages.error(request, f'Error al registrar el pago: {str(e)}')
            return redirect('payments:registrar_pago')
    
    # GET: Mostrar formulario
    socios = Socio.objects.all().order_by('apellido', 'nombre')
    
    context = {
        'metodos_pago': METODOS_PAGO,
        'estados_pago': ESTADOS_PAGO,
        'socios': socios,
    }
    
    return render(request, 'payments/registrar_pago.html', context)