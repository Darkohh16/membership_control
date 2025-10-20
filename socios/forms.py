from django import forms
from .models import Socio
from membership_control.choices import Perfiles

class SociosForm(forms.ModelForm):
    class Meta:
        model = Socio
        field = ['nombre', 'apellido', 'dni_carnet', 'correo', 'celular', 'direccion']
        exclude = ['fecha_registro', 'id']