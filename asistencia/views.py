from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Asistencia
from socios.models import Socio
from .forms import RegistrarAsistenciaForm


def registrar_asistencia_form(request):
    """Vista con formulario para registrar asistencia"""
    if request.method == "POST":
        form = RegistrarAsistenciaForm(request.POST)
        if form.is_valid():
            asistencia = form.save()
            socio = asistencia.socio
            messages.success(
                request, 
                f"✅ Asistencia registrada para {socio.nombre} {socio.apellido}"
            )
            return redirect("asistencia:registrar_asistencia_form")
    else:
        form = RegistrarAsistenciaForm()

    return render(request, "asistencia/registrar_asistencia.html", {"form": form})


def historial_asistencia(request):
    """Vista para ver historial de asistencias"""
    asistencias = (
        Asistencia.objects.all()
        .select_related("socio")
        .order_by("-fecha_hora")[:50]
    )
    return render(request, "asistencia/historial.html", {"asistencias": asistencias})


def buscar_socio(request):
    """Vista para buscar socio por nombre, apellido o DNI"""
    socios = None
    busqueda = None
    
    if request.method == 'POST':
        busqueda = request.POST.get('busqueda', '').strip()
        if busqueda:
            socios = Socio.objects.filter(
                Q(nombre__icontains=busqueda) |
                Q(apellido__icontains=busqueda) |
                Q(dni_carnet__icontains=busqueda)
            ).distinct()
            
            if not socios.exists():
                messages.warning(request, f'No se encontraron socios con "{busqueda}"')
        else:
            messages.error(request, 'Por favor ingresa un término de búsqueda')
    
    return render(request, 'asistencia/buscar_socio.html', {
        'socios': socios,
        'busqueda': busqueda,
    })


def registrar_asistencia_directo(request, socio_id):
    """Vista para registrar asistencia directamente (desde búsqueda)"""
    socio = get_object_or_404(Socio, id=socio_id)
    
    # Crear asistencia
    asistencia = Asistencia.objects.create(
        socio=socio,
        notas=f"Registrado mediante búsqueda"
    )
    
    messages.success(
        request, 
        f'✅ Asistencia registrada para {socio.nombre} {socio.apellido}'
    )
    
    return redirect('asistencia:buscar_socio')