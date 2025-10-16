from django.contrib.auth.models import BaseUserManager, User
from . import constants as user_constants


class UserManager(BaseUserManager):
    def create_user(self, email, perfil, username, full_name, password=None, **extra_fields):
        if not perfil:
            raise ValueError('Se requiere el perfil del usuario')
        if not username:
            raise ValueError('Se requiere el nombre de usuario')
        if not email:
            raise ValueError('Se requiere el email del usuario')
        if not full_name:
            raise ValueError('Se requiere el nombre completo del usuario')

        user = self.model(
            username=username,
            full_name=full_name,
            email=self.normalize_email(email),
            perfil=perfil,
            **extra_fields
        )

        if password is None:
            password = self.make_random_password(
                length=8, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
            )

        user.set_password(password)

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, perfil=1, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    def update_user(self, username, data_user):
        try:
            username = self.get(username=username)

            iduser = data_user.get('username')
            usuario = self.filter(pk=iduser).update(
                full_name=data_user.get('full_name'),
                email=self.normalize_email(data_user.get('email')),
                username=data_user.get('username'),
                password=data_user.get('password'),
            )

            usuario.save()
            return usuario
        except self.model.DoesNotExist:
            raise ValueError('El usuario no existe')