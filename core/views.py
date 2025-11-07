from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import uuid

from socios.models import Socio
from membresias.models import Membresia, TipoMembresia
from payments.models import Pago
from payments.constants import ESTADOS_PAGO

# Create your views here.
@login_required
def home(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    inicio_anio = hoy.replace(month=1, day=1)
    hace_30_dias = hoy - timedelta(days=30)
    
    #------------socios-----------------
    total_socios = Socio.objects.count()
    nuevos_socios_mes = Socio.objects.filter(
        fecha_registro__gte=inicio_mes
    ).count()
    nuevos_socios_30_dias = Socio.objects.filter(
        fecha_registro__gte=hace_30_dias
    ).count()
    
    #socios con membresia activa
    socios_con_membresia_activa = Socio.objects.filter(
        membresias__activa=True
    ).distinct().count()
    
    #socios sin membresia activa
    socios_sin_membresia = total_socios - socios_con_membresia_activa
    
    #----------------------membresias--------------------
    membresias_activas = Membresia.objects.filter(activa=True).count()
    
    #membresias vencidas
    membresias_vencidas = Membresia.objects.filter(
        activa=True,
        fecha_fin__lt=hoy
    ).count()
    
    #membresias por vencer en los proximos 7 dias
    fecha_7_dias = hoy + timedelta(days=7)
    membresias_por_vencer_7 = Membresia.objects.filter(
        activa=True,
        fecha_fin__gte=hoy,
        fecha_fin__lte=fecha_7_dias
    ).count()
    
    #membresias por vencer en los proximos 30 dias
    fecha_30_dias = hoy + timedelta(days=30)
    membresias_por_vencer_30 = Membresia.objects.filter(
        activa=True,
        fecha_fin__gte=hoy,
        fecha_fin__lte=fecha_30_dias
    ).count()
    
    #tipos de membresia mas populares
    tipos_populares = TipoMembresia.objects.annotate(
        total_asignaciones=Count('membresias')
    ).order_by('-total_asignaciones')[:5]
    
    #-------------------finanzas-----------------------
    #ingresos del mes
    ingresos_mes = Pago.objects.filter(
        fecha_pago__gte=inicio_mes,
        estado=ESTADOS_PAGO['Completado']
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    #ingresos del año
    ingresos_anio = Pago.objects.filter(
        fecha_pago__gte=inicio_anio,
        estado=ESTADOS_PAGO['Completado']
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    #ingresos de los ultimos 30 dias
    ingresos_30_dias = Pago.objects.filter(
        fecha_pago__gte=hace_30_dias,
        estado=ESTADOS_PAGO['Completado']
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    #pagos pendientes
    pagos_pendientes = Pago.objects.filter(
        estado=ESTADOS_PAGO['Pendiente']
    ).count()
    
    #monto total pendiente
    monto_pendiente = Pago.objects.filter(
        estado=ESTADOS_PAGO['Pendiente']
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    #promedio de pago
    promedio_pago = Pago.objects.filter(
        estado=ESTADOS_PAGO['Completado']
    ).aggregate(promedio=Avg('monto'))['promedio'] or Decimal('0.00')
    
    #metodos de pago mas usados
    metodos_pago = Pago.objects.filter(
        estado=ESTADOS_PAGO['Completado']
    ).values('metodo_pago').annotate(
        total=Count('id'),
        monto_total=Sum('monto')
    ).order_by('-total')[:5]
    
    #------------------cosas recientes--------------------
    #ultimos pagos
    ultimos_pagos = Pago.objects.select_related(
        'socio', 'membresia__tipo_membresia'
    ).order_by('-fecha_pago')[:5]
    
    #ultimos socios registrados
    ultimos_socios = Socio.objects.order_by('-fecha_registro')[:5]
    
    #-------------------mayday mayday----------------------
    #membresias por vencer proximamente (7 dias)
    alertas_vencimiento = Membresia.objects.filter(
        activa=True,
        fecha_fin__gte=hoy,
        fecha_fin__lte=fecha_7_dias
    ).select_related('socio', 'tipo_membresia')[:10]
    
    context = {
        'total_socios': total_socios,
        'nuevos_socios_mes': nuevos_socios_mes,
        'nuevos_socios_30_dias': nuevos_socios_30_dias,
        'socios_con_membresia_activa': socios_con_membresia_activa,
        'socios_sin_membresia': socios_sin_membresia,

        'membresias_activas': membresias_activas,
        'membresias_vencidas': membresias_vencidas,
        'membresias_por_vencer_7': membresias_por_vencer_7,
        'membresias_por_vencer_30': membresias_por_vencer_30,
        'tipos_populares': tipos_populares,

        'ingresos_mes': ingresos_mes,
        'ingresos_anio': ingresos_anio,
        'ingresos_30_dias': ingresos_30_dias,
        'pagos_pendientes': pagos_pendientes,
        'monto_pendiente': monto_pendiente,
        'promedio_pago': promedio_pago,
        'metodos_pago': metodos_pago,

        'ultimos_pagos': ultimos_pagos,
        'ultimos_socios': ultimos_socios,

        'alertas_vencimiento': alertas_vencimiento,
    }
    
    return render(request, 'core/dashboard.html', context)
