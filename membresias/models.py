from django.db import models
from django.core.validators import MinValueValidator
from socios.models import Socio
from datetime import timedelta


class TipoMembresia(models.Model):
    """
    Modelo para representar los tipos de membresías disponibles.
    US11: Como administrador, quiero gestionar tipos de membresías.
    """
    
    # Opciones de duración
    DURACION_MENSUAL = 30
    DURACION_TRIMESTRAL = 90
    DURACION_SEMESTRAL = 180
    DURACION_ANUAL = 365
    
    DURACIONES_CHOICES = [
        (DURACION_MENSUAL, 'Mensual (30 días)'),
        (DURACION_TRIMESTRAL, 'Trimestral (3 meses)'),
        (DURACION_SEMESTRAL, 'Semestral (6 meses)'),
        (DURACION_ANUAL, 'Anual (12 meses)'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del tipo de membresía (ej: Básica, Premium, Gold)"
    )
    
    duracion_dias = models.IntegerField(
        choices=DURACIONES_CHOICES,
        default=DURACION_MENSUAL,
        help_text="Duración de la membresía en días"
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Precio de la membresía en soles (S/)"
    )
    
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción y beneficios de la membresía"
    )
    
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el tipo de membresía está activo y disponible"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tipo de Membresía"
        verbose_name_plural = "Tipos de Membresías"
        ordering = ['precio', 'duracion_dias']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_duracion_dias_display()} - S/ {self.precio}"
    
    def get_duracion_meses(self):
        """Retorna la duración aproximada en meses"""
        return round(self.duracion_dias / 30, 1)


class Membresia(models.Model):
    """
    Modelo para representar las membresías asignadas a los socios.
    Relaciona un socio con un tipo de membresía específico.
    """
    
    socio = models.ForeignKey(
        Socio,
        on_delete=models.CASCADE,
        related_name='membresias',
        help_text="Socio al que pertenece la membresía"
    )
    
    tipo_membresia = models.ForeignKey(
        TipoMembresia,
        on_delete=models.PROTECT,
        related_name='membresias',
        help_text="Tipo de membresía asignada"
    )
    
    fecha_inicio = models.DateField(
        help_text="Fecha de inicio de la membresía"
    )
    
    fecha_fin = models.DateField(
        help_text="Fecha de fin de la membresía"
    )
    
    activa = models.BooleanField(
        default=False,  # Cambiado a False - se activa al pagar
        help_text="Indica si la membresía está activa actualmente"
    )
    
    pagada = models.BooleanField(
        default=False,
        help_text="Indica si la membresía ha sido pagada"
    )
    
    observaciones = models.TextField(
        blank=True,
        help_text="Observaciones o notas sobre la membresía"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Membresía"
        verbose_name_plural = "Membresías"
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['socio', 'activa']),
            models.Index(fields=['fecha_fin', 'activa']),
        ]
    
    def __str__(self):
        return f"{self.socio.nombre} {self.socio.apellido} - {self.tipo_membresia.nombre}"
    
    def dias_restantes(self):
        """Calcula los días restantes de la membresía"""
        from datetime import date
        if self.activa and self.fecha_fin >= date.today():
            return (self.fecha_fin - date.today()).days
        return 0
    
    def esta_vencida(self):
        """Verifica si la membresía está vencida"""
        from datetime import date
        return self.fecha_fin < date.today()
    
    def esta_por_vencer(self, dias=7):
        """Verifica si la membresía está por vencer en los próximos X días"""
        from datetime import date
        if not self.activa or self.esta_vencida():
            return False
        dias_restantes = self.dias_restantes()
        return 0 < dias_restantes <= dias
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular la fecha_fin automáticamente
        si no se proporciona.
        """
        if not self.fecha_fin and self.fecha_inicio and self.tipo_membresia:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.tipo_membresia.duracion_dias)
        
        # Desactivar otras membresías activas del mismo socio al activar una nueva
        if self.activa:
            Membresia.objects.filter(
                socio=self.socio,
                activa=True
            ).exclude(pk=self.pk).update(activa=False)
        
        super().save(*args, **kwargs)
