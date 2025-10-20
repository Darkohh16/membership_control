from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Asistencia
from accounts.models import Usuario
from .forms import RegistrarAsistenciaForm  # formulario para registrar asistencia


# Vista con formulario para registrar asistencia
def registrar_asistencia_form(request):
    if request.method == "POST":
        form = RegistrarAsistenciaForm(request.POST)
        if form.is_valid():
            asistencia = form.save(commit=False)
            # Por ahora, asignamos None si no hay login de recepcionista
            asistencia.registrado_por = getattr(request, "user", None)
            asistencia.save()
            messages.success(
                request, f"Asistencia registrada para {asistencia.socio.username}"
            )
            return redirect("asistencia:registrar_asistencia_form")
    else:
        form = RegistrarAsistenciaForm()

    return render(request, "asistencia/registrar_asistencia.html", {"form": form})


# Vista para ver historial de asistencias
def historial_asistencia(request):
    asistencias = (
        Asistencia.objects.all().select_related("socio").order_by("-fecha_hora")[:50]
    )
    return render(request, "asistencia/historial.html", {"asistencias": asistencias})

# Vista para buscar socio por nombre/usuario
def buscar_socio(request):
    from django.db.models import Q
    
    socios = None
    busqueda = None
    
    if request.method == 'POST':
        busqueda = request.POST.get('busqueda', '').strip()
        if busqueda:
            socios = Usuario.objects.filter(
                Q(username__icontains=busqueda) |
                Q(first_name__icontains=busqueda) |
                Q(last_name__icontains=busqueda),
                perfil=2  # Solo usuarios/socios
            ).distinct()
            
            if not socios.exists():
                messages.warning(request, f'No se encontraron socios con "{busqueda}"')
        else:
            messages.error(request, 'Por favor ingresa un término de búsqueda')
    
    return render(request, 'asistencia/buscar_socio.html', {
        'socios': socios,
        'busqueda': busqueda,
    })


# Vista para registrar asistencia directamente (desde búsqueda)
def registrar_asistencia_directo(request, socio_username):
    socio = get_object_or_404(Usuario, username=socio_username, perfil=2)
    
    # Crear asistencia
    asistencia = Asistencia.objects.create(
        socio=socio,
        notas=f"Registrado mediante búsqueda"
    )
    
    messages.success(
        request, 
        f'✅ Asistencia registrada para {socio.get_full_name() or socio.username}'
    )
    
    return redirect('asistencia:buscar_socio')
