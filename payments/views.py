from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, Exists, OuterRef
from django.db import transaction
from decimal import Decimal
from datetime import datetime, timedelta

from payments.models import Pago
from payments.constants import METODOS_PAGO, ESTADOS_PAGO
from socios.models import Socio
from membresias.models import Membresia


@login_required
def listar_pagos(request):
    """
    Vista para listar todos los pagos registrados.
    """
    pagos = Pago.objects.all().select_related('socio', 'membresia__tipo_membresia', 'registrado_por').order_by('-fecha_pago')
    
    context = {
        'pagos': pagos,
    }
    
    return render(request, 'payments/listar_pagos.html', context)


@login_required
def detalle_pago(request, pago_id):
    """
    Vista para ver el detalle de un pago específico.
    """
    pago = get_object_or_404(
        Pago.objects.select_related('socio', 'membresia__tipo_membresia', 'registrado_por'),
        pk=pago_id
    )
    
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
            concepto = request.POST.get('concepto', '')
            notas = request.POST.get('notas', '')
            membresia_id = request.POST.get('membresia', '')
            
            # El estado siempre será "Completado" (2) automáticamente
            estado = 2
            
            # Validaciones
            if not socio_id or not monto or not metodo_pago:
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
                return redirect('payments:registrar_pago')
            
            # Validar monto
            monto_decimal = Decimal(monto)
            if monto_decimal <= 0:
                messages.error(request, 'El monto debe ser mayor a 0.')
                return redirect('payments:registrar_pago')
            
            # Obtener el socio
            socio = Socio.objects.get(id=socio_id)
            
            # Obtener membresía si se seleccionó
            membresia = None
            if membresia_id:
                try:
                    membresia = Membresia.objects.get(id=membresia_id)
                    
                    # Verificar que la membresía no esté ya pagada
                    if membresia.pagada:
                        messages.error(request, 'Esta membresía ya ha sido pagada.')
                        return redirect('payments:registrar_pago')
                        
                except Membresia.DoesNotExist:
                    messages.error(request, 'La membresía seleccionada no existe.')
                    return redirect('payments:registrar_pago')
            else:
                # Validar que se haya seleccionado una membresía (obligatorio)
                messages.error(request, 'Debe seleccionar una membresía. Los pagos deben estar asociados a una membresía.')
                return redirect('payments:registrar_pago')
            
            # Usar transacción para garantizar atomicidad
            with transaction.atomic():
                # Crear el pago (estado siempre será 2 = Completado)
                pago = Pago.objects.create(
                    socio=socio,
                    monto=monto_decimal,
                    metodo_pago=int(metodo_pago),
                    estado=2,  # Siempre completado
                    concepto=concepto,
                    notas=notas,
                    registrado_por=request.user,
                    membresia=membresia  # Asociar membresía
                )
                
                # ACTIVAR LA MEMBRESÍA después del pago
                if membresia:
                    membresia.activa = True
                    membresia.pagada = True
                    membresia.save()  # El método save() desactivará otras membresías activas
            
            messages.success(request, f'Pago registrado exitosamente. Recibo: {pago.numero_recibo}. La membresía ha sido activada.')
            # POST-Redirect-GET pattern: Redirigir después de procesar POST
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
    # Mostrar todos los socios (el filtro se hace en el API que devuelve solo membresías pendientes)
    socios = Socio.objects.all().order_by('apellido', 'nombre')
    
    context = {
        'metodos_pago': METODOS_PAGO,
        'socios': socios,
    }
    
    return render(request, 'payments/registrar_pago.html', context)

    @login_required
def historial_pagos_socio(request, socio_id):
    """
    Vista para mostrar el historial de pagos de un socio específico.
    US06: Como administrador, quiero ver un historial de pagos por socio.
    """
    # Verificar que el usuario sea administrador
    if request.user.perfil != 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para ver esta página.')
        return redirect('dashboard')  # Redirigir a una página segura

    socio = get_object_or_404(Socio, id=socio_id)
    
    # Queryset optimizado para obtener los pagos del socio
    pagos = Pago.objects.filter(socio=socio).select_related(
        'membresia__tipo_membresia', 
        'registrado_por'
    ).order_by('-fecha_pago')
    
    context = {
        'socio': socio,
        'pagos': pagos,
    }
    
    return render(request, 'payments/historial_pagos_socio.html', context)