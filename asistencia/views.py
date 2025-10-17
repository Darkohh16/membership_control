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
            asistencia.registrado_por = getattr(request, 'user', None)
            asistencia.save()
            messages.success(request, f"Asistencia registrada para {asistencia.socio.username}")
            return redirect('asistencia:registrar_asistencia_form')
    else:
        form = RegistrarAsistenciaForm()
    
    return render(request, "asistencia/registrar_asistencia.html", {"form": form})
