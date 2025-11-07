from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
import uuid

from django.views.decorators.cache import never_cache

from membresias.models import Membresia
from socios.forms import SociosForm
from .models import *


@login_required
def socios_view(request):
    #Obtener datos
    socios_list = Socio.objects.all()

    #FILTROS

    #------------------------------
    paginator = Paginator(socios_list, 10)
    page = request.GET.get('page')
    socios = paginator.get_page(page)

    context = {
        'socios': socios,
    }

    return render(request, 'socios/socios_general.html', context)

@never_cache
@login_required
def nuevo_socio(request):
    if request.method == 'POST':
        form = SociosForm(request.POST)
        if form.is_valid():
            try:
                socio = form.save(commit=False)
                socio.id = uuid.uuid4()
                socio.save()

                messages.success(request, 'Socio creado exitosamente')
                return redirect('socios_general')
            except Exception as e:
                messages.error(request, f'Error al crear Socio: {str(e)}')
        else:
            messages.warning(request, f'Hay errores en el formulario')

    else:
        form = SociosForm()

    context = {'form': form}

    return render(request, 'socios/nuevo_socio.html', context)

@login_required
def editar_socio(request, id):
    socio = get_object_or_404(Socio, id=id)
    if request.method == 'POST':
        form = SociosForm(request.POST, instance=socio)
        form.fields.pop('fecha_nacimiento', None)
        if form.is_valid():
            try:
                form.save()

                messages.success(request, 'Socio actualizado exitosamente')
                return redirect('editar_socio', id=id)
            except Exception as e:
                messages.error(request, f'Error al actualizar Socio: {str(e)}')
        else:
            messages.warning(request, f'Hay errores en el formulario: {str(form.errors)}')
    else:
        form = SociosForm(instance=socio)

    context = {
        'form': form,
        'socio': socio,
    }
    return render(request, 'socios/editar_socio.html', context)

@login_required
def socios_por_vencer(request):
    d = 30
    por_vencer = [
        s for s in Membresia.objects.filter(activa=True).select_related('socio', 'tipo_membresia') if s.esta_por_vencer(dias=d)
    ]

    context = {
        'membresias': por_vencer,
    }

    return render(request, 'socios/socios_por_vencer.html', context)