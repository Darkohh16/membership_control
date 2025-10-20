from django.db import models
from datetime import date, timedelta


class TipoMembresia(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    duracion_dias = models.PositiveIntegerField(default=30)  # Ejemplo: 30, 90, 365
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - S/ {self.precio}"


class Socio(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ]

    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)

    tipo_membresia = models.ForeignKey(TipoMembresia, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateField(default=date.today)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    def save(self, *args, **kwargs):
        # Si no tiene fecha_fin, se calcula automáticamente según el tipo de membresía
        if self.fecha_inicio and self.tipo_membresia and not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.tipo_membresia.duracion_dias)
        super().save(*args, **kwargs)

    def dias_restantes(self):
        """Devuelve cuántos días quedan para que finalice la membresía"""
        if self.fecha_fin:
            return (self.fecha_fin - date.today()).days
        return None

    def __str__(self):
        return f"{self.nombre} ({self.tipo_membresia})"


class Pago(models.Model):
    METODOS = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('yape', 'Yape/Plin'),
    ]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pago de {self.socio.nombre} - {self.fecha_pago} - S/ {self.monto}"

