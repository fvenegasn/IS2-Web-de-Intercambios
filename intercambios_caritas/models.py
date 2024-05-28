from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# aca iria el back ¿


class Usuario(AbstractUser):

    # login_attempts = models.IntegerField(default=0)

    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    nacimiento = models.DateField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        telefono = kwargs.pop('telefono', None)
        direccion = kwargs.pop('direccion', None)
        nacimiento = kwargs.pop('nacimiento', None)
        super().__init__(*args, **kwargs)
        if telefono is not None:
            self.telefono = telefono
        if direccion is not None:
            self.direccion = direccion
        if nacimiento is not None:
            self.nacimiento = nacimiento

    def __str__(self):
        return self.username


def get_default_user():
    return Usuario.objects.first().id


class Publicacion(models.Model):
    """ opciones validas que se pueden elegir en el formulario de publicacion
    de ser necesario estas listas podrian ser otra tabla en la base de datos 
    para que el usuario modifique las opciones"""

    PUNTOS_ENC = [
        ('Negociable', 'Negociable'),
        ('La Plata', 'La Plata'),
        ('CABA', 'CABA'),
        ('Quilmes', 'Quilmes'),
        ('Temperley', 'Temperley'),
    ]
    CATEGORIAS = [
        ('Alimentos', 'Alimentos'),
        ('Ropa', 'Ropa'),
        ('Utiles escolares', 'Utiles escolares'),
        ('Artículos de limpieza', 'Artículos de limpieza'),
    ]
    ESTADOS = [
        ('Sin especificar', 'Sin especificar'),
        ('Usado', 'Usado'),
        ('Nuevo', 'Nuevo'),
    ]

    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(
        max_length=280, blank=True, null=False, default="Sin descripción")
    imagen = models.ImageField()
    categoria = models.CharField(
        max_length=50, blank=False, null=False, choices=CATEGORIAS, default="Otros")
    estado = models.CharField(
        max_length=50, blank=False, null=False, choices=ESTADOS, default=ESTADOS[0][0])
    punto_encuentro = models.CharField(
        max_length=50, blank=False, null=False, choices=PUNTOS_ENC, default=PUNTOS_ENC[0][0])
    # TODO -> ver como integrar con models.ForeignKey
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, default=get_default_user)

    def __str__(self):
        return self.nombre
