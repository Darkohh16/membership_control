from django.db import models

class Perfiles(models.IntegerChoices):
    ADMINISTRADOR = 1, "Administrador"
    USUARIO = 2, "Usuario"
    RECEPCIONISTA = 3, "Recepcionista"