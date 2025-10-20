from django.db import models

class Socio(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)
    dni_carnet = models.CharField(max_length=12, blank=False, null=False)
    correo = models.EmailField(unique=True, blank=False, null=False)
    celular = models.CharField(max_length=9, blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=False, null=True)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    fecha_registro = models.DateField(auto_now_add=True, blank=False, null=False)

    class Meta:
        db_table = 'socios'
        ordering = ['apellido']

    def __str__(self):
        return self.apellido