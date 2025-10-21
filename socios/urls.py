from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from socios.views import *
from core.views import *


urlpatterns = [
    path('mostrar/', socios_view, name='socios_general'),
    path('agregar/', nuevo_socio, name='nuevo_socio'),
    path('<uuid:id>/editar/', editar_socio, name='editar_socio'),
]