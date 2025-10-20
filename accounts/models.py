from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.helpers import avatar_path
from accounts.managers import UserManager
from membership_control.choices import *

# Create your models here.
class Usuario(AbstractUser):
    username = models.CharField(max_length=25, blank=False, null=False,
                                unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, null=False)
    perfil = models.IntegerField(choices=Perfiles, null=False)
    avatar = models.ImageField(
        upload_to=avatar_path,
        blank=True, null=True,
        help_text="Imagen de perfil del usuario.")
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario',
    )

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.last_name

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