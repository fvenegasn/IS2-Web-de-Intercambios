from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# aca iria el back ¿

class Usuario(AbstractUser):

    #login_attempts = models.IntegerField(default=0)

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

class Publicacion(models.Model):

    nombre = models.CharField(max_length=50, blank=False, null=False)
    categoria = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=280, blank=True,null=True)
    imagen = models.ImageField()
    estado = models.CharField(max_length=50, blank=True, null=True)
    punto_encuentro = models.CharField(max_length=50, blank=True, null=True)
    usuario_dni = models.CharField(max_length=150,default="")
    usuario_nombre = models.CharField(max_length=150,default="")

    def __str__(self):
        return self.nombre
