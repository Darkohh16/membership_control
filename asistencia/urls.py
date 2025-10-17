from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
     path('registrar-form/', views.registrar_asistencia_form, name='registrar_asistencia_form'),
]