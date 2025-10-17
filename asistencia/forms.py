from django import forms
from accounts.models import Usuario
from .models import Asistencia

class RegistrarAsistenciaForm(forms.ModelForm):
    # Mostrar solo usuarios/socios
    socio = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(perfil=2),  # 2 = Usuario/socio
        label="Selecciona un socio"
    )

    class Meta:
        model = Asistencia
        fields = ['socio', 'notas']