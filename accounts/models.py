from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.helpers import avatar_path
from accounts.managers import UserManager


# Create your models here.
class Perfil(models.Model):
    perfil_id = models.IntegerField(primary_key=True)
    perfil_nombre = models.CharField(max_length=100, null=False)

    def __str__(self):
        return '%d: %s' % (self.perfil_id, self.perfil_nombre)

    class Meta:
        db_table = 'perfiles'


class Usuario(AbstractUser):
    username = models.CharField(max_length=25, blank=False, null=False,
                                unique=True, primary_key=True)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, null=False)
    perfil = models.ForeignKey(Perfil, null = False, on_delete=models.RESTRICT, related_name='perfiles_usuarios')
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
    REQUIRED_FIELDS = ['full_name', 'perfil', 'email']

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.full_name