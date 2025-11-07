from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from membresias.models import TipoMembresia, Membresia
from socios.models import Socio
from datetime import timedelta


@login_required
def listar_tipos(request):
    """
    Vista para listar todos los tipos de membresía.
    """
    tipos = TipoMembresia.objects.all().order_by('precio', 'duracion_dias')
    
    context = {
        'tipos': tipos,
    }
    return render(request, 'membresias/listar_tipos.html', context)


@login_required
def crear_tipo(request):
    """
    Vista para crear un nuevo tipo de membresía (solo admin).
    """
    if not request.user.perfil == 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('listar_tipos')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        duracion_dias = request.POST.get('duracion_dias')
        precio = request.POST.get('precio')
        activo = request.POST.get('activo') == 'on'
        
        # Validación
        if not nombre or not duracion_dias or not precio:
            messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            return render(request, 'membresias/crear_tipo.html')
        
        try:
            tipo = TipoMembresia.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                duracion_dias=int(duracion_dias),
                precio=float(precio),
                activo=activo
            )
            messages.success(request, f'Tipo de membresía "{tipo.nombre}" creado exitosamente.')
            return redirect('listar_tipos')
        except Exception as e:
            messages.error(request, f'Error al crear el tipo: {str(e)}')
    
    return render(request, 'membresias/crear_tipo.html')


@login_required
def editar_tipo(request, tipo_id):
    """
    Vista para editar un tipo de membresía existente (solo admin).
    """
    if not request.user.perfil == 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('listar_tipos')
    
    tipo = get_object_or_404(TipoMembresia, pk=tipo_id)
    
    if request.method == 'POST':
        tipo.nombre = request.POST.get('nombre')
        tipo.descripcion = request.POST.get('descripcion', '')
        tipo.duracion_dias = int(request.POST.get('duracion_dias'))
        tipo.precio = float(request.POST.get('precio'))
        tipo.activo = request.POST.get('activo') == 'on'
        
        try:
            tipo.save()
            messages.success(request, f'Tipo de membresía "{tipo.nombre}" actualizado exitosamente.')
            return redirect('listar_tipos')
        except Exception as e:
            messages.error(request, f'Error al actualizar el tipo: {str(e)}')
    
    context = {
        'tipo': tipo,
    }
    return render(request, 'membresias/editar_tipo.html', context)


@login_required
def asignar_membresia(request):
    """
    Vista para asignar una membresía a un socio.
    """
    if not request.user.perfil == 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('listar_tipos')
    
    from datetime import date
    socios = Socio.objects.all().order_by('apellido', 'nombre')
    tipos = TipoMembresia.objects.filter(activo=True)
    
    if request.method == 'POST':
        socio_id = request.POST.get('socio')
        tipo_id = request.POST.get('tipo_membresia')
        fecha_inicio = request.POST.get('fecha_inicio')
        observaciones = request.POST.get('observaciones', '')
        
        if not socio_id or not tipo_id or not fecha_inicio:
            messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            return render(request, 'membresias/asignar_membresia.html', {
                'socios': socios,
                'tipos': tipos,
                'today': date.today(),
            })
        
        try:
            socio = get_object_or_404(Socio, pk=socio_id)
            tipo = get_object_or_404(TipoMembresia, pk=tipo_id)
            
            # Validar que no tenga membresías activas
            membresias_activas = Membresia.objects.filter(socio=socio, activa=True)
            if membresias_activas.exists():
                membresia_activa = membresias_activas.first()
                messages.error(request, f'Este socio ya tiene una membresía activa ({membresia_activa.tipo_membresia.nombre}). Debe desactivarla primero para asignar una nueva.')
                return render(request, 'membresias/asignar_membresia.html', {
                    'socios': socios,
                    'tipos': tipos,
                    'today': date.today(),
                })
            
            # Validar que la fecha no sea anterior a hoy
            from datetime import datetime
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            
            if fecha_inicio_dt < date.today():
                messages.error(request, 'La fecha de inicio no puede ser anterior a la fecha actual.')
                return render(request, 'membresias/asignar_membresia.html', {
                    'socios': socios,
                    'tipos': tipos,
                    'today': date.today(),
                })
            
            fecha_fin = fecha_inicio_dt + timedelta(days=tipo.duracion_dias)
            
            membresia = Membresia.objects.create(
                socio=socio,
                tipo_membresia=tipo,
                fecha_inicio=fecha_inicio_dt,
                fecha_fin=fecha_fin,
                activa=False,  # NO se activa hasta que se pague
                pagada=False,  # Membresía aún no pagada
                observaciones=observaciones
            )
            
            messages.success(request, f'Membresía asignada exitosamente a {socio.nombre} {socio.apellido}. Recuerde registrar el pago para activarla.')
            return redirect('listar_membresias_socio', socio_id=socio.id)
        except Exception as e:
            messages.error(request, f'Error al asignar membresía: {str(e)}')
    
    context = {
        'socios': socios,
        'tipos': tipos,
        'today': date.today(),
    }
    return render(request, 'membresias/asignar_membresia.html', context)


@login_required
def listar_membresias_socio(request, socio_id):
    """
    Vista para listar todas las membresías de un socio.
    """
    socio = get_object_or_404(Socio, pk=socio_id)
    membresias = Membresia.objects.filter(socio=socio).order_by('-fecha_inicio')
    
    context = {
        'socio': socio,
        'membresias': membresias,
    }
    return render(request, 'membresias/listar_membresias_socio.html', context)


@login_required
def desactivar_membresia(request, membresia_id):
    """
    Vista para desactivar una membresía.
    """
    if not request.user.perfil == 1:  # 1 = Administrador
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('listar_tipos')
    
    membresia = get_object_or_404(Membresia, pk=membresia_id)
    membresia.activa = False
    membresia.save()
    
    messages.success(request, 'Membresía desactivada exitosamente.')
    return redirect('listar_membresias_socio', socio_id=membresia.socio.id)


@login_required
def api_membresias_socio(request, socio_id):
    """
    API endpoint para obtener las membresías pendientes de pago de un socio.
    Retorna JSON con la información de las membresías que aún no han sido pagadas.
    """
    try:
        socio = get_object_or_404(Socio, pk=socio_id)
        # Solo membresías NO pagadas (pendientes de pago)
        membresias = Membresia.objects.filter(
            socio=socio, 
            pagada=False
        ).select_related('tipo_membresia')
        
        membresias_data = []
        for membresia in membresias:
            # Determinar el estado de la membresía
            dias_restantes = membresia.dias_restantes()
            if membresia.esta_vencida():
                estado_text = 'Vencida (Sin pagar)'
                estado_class = 'bg-red-100 text-red-800'
            elif dias_restantes <= 7:
                estado_text = f'Pendiente de pago'
                estado_class = 'bg-yellow-100 text-yellow-800'
            else:
                estado_text = f'Pendiente de pago'
                estado_class = 'bg-yellow-100 text-yellow-800'
            
            membresias_data.append({
                'id': membresia.id,
                'tipo_nombre': membresia.tipo_membresia.nombre,
                'tipo_precio': float(membresia.tipo_membresia.precio),
                'fecha_inicio': membresia.fecha_inicio.strftime('%d/%m/%Y'),
                'fecha_fin': membresia.fecha_fin.strftime('%d/%m/%Y'),
                'dias_restantes': dias_restantes,
                'estado_text': estado_text,
                'estado_class': estado_class,
            })
        
        return JsonResponse({
            'success': True,
            'membresias': membresias_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
