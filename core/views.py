from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
import uuid

# Create your views here.
@login_required
def home(request):
    #Vista para la pagina principal

    #Obtener datos para los widgets

    #------------------------------
    return render(request, 'core/dashboard.html')


@login_required
def debug_perfil(request):
    """Vista temporal para verificar el perfil del usuario"""
    return render(request, 'debug_perfil.html')
