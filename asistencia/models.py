from django.db import models
from django.conf import settings
from django.utils import timezone


class Asistencia(models.Model):
    socio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Socio")
    fecha_hora = models.DateTimeField(default=timezone.now, verbose_name="Fecha y Hora de Entrada")
    metodo_registro = models.CharField(
        max_length=20,
        choices=[
            ('MANUAL', 'Búsqueda Manual'),
            ('QR', 'Código QR'),
        ],
        default='MANUAL',
        verbose_name="Método de Registro"
    )
    notas = models.TextField(blank=True, null=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.socio.username} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"