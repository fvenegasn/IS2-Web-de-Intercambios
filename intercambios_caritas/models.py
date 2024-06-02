import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from multiselectfield import MultiSelectField
from django.utils import timezone


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
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=280, blank=True, null=False, default="Sin descripción")
    imagen = models.ImageField()
    categoria = models.CharField(max_length=50, blank=False, null=False, choices=CATEGORIAS, default="Otros")
    estado = models.CharField(max_length=50, blank=False, null=False, choices=ESTADOS, default=ESTADOS[0][0])
    punto_encuentro = models.CharField(max_length=50, blank=False, null=False, choices=PUNTOS_ENC, default=PUNTOS_ENC[0][0])
    dias_convenientes = MultiSelectField(choices=DIAS_SEMANA, blank=True, max_length=100)
    franja_horaria = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=get_default_user)
    
    FRANJA_HORARIA_REGEX = r'^entre las (\d{2}):(\d{2}) y las (\d{2}):(\d{2})$'

    def clean(self):
        super().clean()
        if self.franja_horaria:
            match = re.match(self.FRANJA_HORARIA_REGEX, self.franja_horaria)
            if not match:
                raise ValidationError("El formato de la franja horaria debe ser 'entre las HH:MM y las HH:MM'.")
            inicio_hora, inicio_minuto, fin_hora, fin_minuto = match.groups()
            if int(inicio_hora) > int(fin_hora) or (int(inicio_hora) == int(fin_hora) and int(inicio_minuto) >= int(fin_minuto)):
                raise ValidationError("La hora de inicio debe ser antes que la hora de finalización.")
            if int(inicio_hora) < 0 or int(fin_hora) > 23 or int(inicio_minuto) < 0 or int(fin_minuto) > 59:
                raise ValidationError("Las horas deben estar entre 00 y 23, y los minutos entre 00 y 59.")

    def __str__(self):
        return self.nombre

class Intercambio(models.Model):
    publicacion_ofertante = models.ForeignKey('Publicacion', related_name='ofertas_realizadas', on_delete=models.CASCADE)
    publicacion_demandada = models.ForeignKey('Publicacion', related_name='ofertas_recibidas', on_delete=models.CASCADE)
    centro_encuentro = models.CharField(max_length=50, choices=Publicacion.PUNTOS_ENC)
    dias_convenientes = MultiSelectField(choices=Publicacion.DIAS_SEMANA, blank=True, max_length=100)
    franja_horaria_inicio = models.TimeField()
    franja_horaria_fin = models.TimeField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    aceptada = models.BooleanField(default=False)

    def __str__(self):
        return f"Intercambio de {self.publicacion_ofertante.nombre} por {self.publicacion_demandada.nombre}"

    def es_valida(self):
        return (self.publicacion_ofertante.categoria == self.publicacion_demandada.categoria and
                self.publicacion_ofertante.usuario != self.publicacion_demandada.usuario and
                not Intercambio.objects.filter(publicacion_demandada=self.publicacion_demandada, aceptada=True).exists())