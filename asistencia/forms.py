from django import forms
from socios.models import Socio
from .models import Asistencia


class RegistrarAsistenciaForm(forms.ModelForm):
    """Formulario para registrar asistencia de socios"""
    
    socio = forms.ModelChoiceField(
        queryset=Socio.objects.all().order_by('apellido', 'nombre'),
        label="Selecciona un socio",
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
        }),
        empty_label="-- Seleccione un socio --"
    )
    
    notas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observaciones adicionales (opcional)...'
        }),
        label="Notas"
    )

    class Meta:
        model = Asistencia
        fields = ['socio', 'notas']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar cómo se muestran los socios en el dropdown
        self.fields['socio'].label_from_instance = lambda obj: f"{obj.apellido}, {obj.nombre} - DNI: {obj.dni_carnet}"