from django.db import models
from django.utils import timezone
from socios.models import Socio


class Asistencia(models.Model):
    socio = models.ForeignKey(
        Socio,
        on_delete=models.CASCADE,
        verbose_name="Socio",
        related_name="asistencias"
    )
    fecha_hora = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha y Hora de Entrada"
    )
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas"
    )

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ['-fecha_hora']
        db_table = 'asistencias'

    def __str__(self):
        return f"{self.socio.nombre} {self.socio.apellido} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

    def get_socio_nombre_completo(self):
        """Retorna el nombre completo del socio"""
        return f"{self.socio.nombre} {self.socio.apellido}"