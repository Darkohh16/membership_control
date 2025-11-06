from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from payments.constants import METODOS_PAGO, ESTADOS_PAGO
from payments.managers import PagoManager
from payments.helpers import generar_numero_recibo


# Create your models here.
class Pago(models.Model):
    """
    Modelo para registrar los pagos de membresías.
    US05: Como administrador, quiero registrar los pagos de membresías,
    para mantener control financiero.
    """
    numero_recibo = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text="Número de recibo único generado automáticamente"
    )
    
    # Relación con el socio que realiza el pago
    socio = models.ForeignKey(
        'socios.Socio',
        on_delete=models.CASCADE,
        related_name='pagos',
        help_text="Socio que realiza el pago"
    )
    
    # Relación con la membresía (requerido para nuevos pagos)
    membresia = models.ForeignKey(
        'membresias.Membresia',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='pagos',
        help_text="Membresía asociada al pago"
    )
    
    # Fecha del pago
    fecha_pago = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se registró el pago"
    )
    
    # Monto del pago
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Monto del pago en soles (S/)"
    )
    
    # Método de pago
    metodo_pago = models.IntegerField(
        choices=[(v, k) for k, v in METODOS_PAGO.items()],
        help_text="Método utilizado para realizar el pago"
    )
    
    # Estado del pago
    estado = models.IntegerField(
        choices=[(v, k) for k, v in ESTADOS_PAGO.items()],
        default=2,  # Por defecto: Completado
        help_text="Estado actual del pago"
    )
    
    # Información adicional
    concepto = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Concepto o descripción del pago"
    )
    
    notas = models.TextField(
        blank=True,
        null=True,
        help_text="Notas adicionales sobre el pago"
    )
    
    # Usuario que registra el pago (generalmente un administrador)
    registrado_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pagos_registrados',
        help_text="Administrador que registró el pago"
    )
    
    # Fecha de creación y actualización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Manager personalizado
    objects = PagoManager()
    
    class Meta:
        db_table = 'pagos'
        ordering = ['-fecha_pago']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        indexes = [
            models.Index(fields=['-fecha_pago']),
            models.Index(fields=['socio', '-fecha_pago']),
            models.Index(fields=['metodo_pago']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"Pago {self.numero_recibo} - {self.socio.nombre} {self.socio.apellido} - S/ {self.monto}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar automáticamente
        el número de recibo si no existe.
        """
        if not self.numero_recibo:
            self.numero_recibo = generar_numero_recibo()
        super().save(*args, **kwargs)
    
    def get_metodo_pago_display_custom(self):
        """
        Obtiene el nombre del método de pago.
        """
        for nombre, valor in METODOS_PAGO.items():
            if valor == self.metodo_pago:
                return nombre
        return "Desconocido"
    
    def get_estado_display_custom(self):
        """
        Obtiene el nombre del estado del pago.
        """
        for nombre, valor in ESTADOS_PAGO.items():
            if valor == self.estado:
                return nombre
        return "Desconocido"
    
    def es_pago_membresia(self):
        """
        Verifica si el pago está asociado a una membresía.
        """
        return self.membresia is not None
    
    def get_socio_nombre_completo(self):
        """
        Obtiene el nombre completo del socio.
        """
        return f"{self.socio.nombre} {self.socio.apellido}"
    
    def get_estado_badge_class(self):
        """
        Retorna la clase CSS para el badge según el estado.
        """
        estados_class = {
            1: 'bg-yellow-100 text-yellow-800',  # Pendiente
            2: 'bg-green-100 text-green-800',    # Completado
            3: 'bg-red-100 text-red-800',        # Cancelado
        }
        return estados_class.get(self.estado, 'bg-gray-100 text-gray-800')
