import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from multiselectfield import MultiSelectField
from django.utils import timezone
from abc import ABC, abstractmethod
import datetime

# Create your models here.


class Usuario(AbstractUser):

    # login_attempts = models.IntegerField(default=0)

    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    nacimiento = models.DateField(blank=True, null=True)

    class Types(models.TextChoices):
        Administrador = "Administrador", "Administrador"
        Usuario = "Usuario", "Usuario"
        Moderador = "Moderador", "Moderador"

    rol = models.CharField(
        max_length=20, choices=Types.choices, default=Types.Usuario
    )

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
    
    def isAdmin(self):
        return self.rol.upper() == 'ADMINISTRADOR'
    
    def isUser(self):
        return self.rol.upper() == 'USUARIO'
    
    def isModerador(self):
        return self.rol.upper() == 'MODERADOR'
    
    def getRol(self):
        return self.rol


def get_default_user():
    return Usuario.objects.first().id


class Publicacion(models.Model):
    """
    Define la estructura inicial para todas las publicaciones
    """

    # Puntos de encuentro posibles
    PUNTOS_ENC = [
        ('La Plata', 'La Plata'),
        ('CABA', 'CABA'),
        ('Quilmes', 'Quilmes'),
        ('Temperley', 'Temperley'),
    ]

    # Categorías posibles
    CATEGORIAS = [
        ('Alimentos', 'Alimentos'),
        ('Ropa', 'Ropa'),
        ('Utiles escolares', 'Utiles escolares'),
        ('Artículos de limpieza', 'Artículos de limpieza'),
    ]

    # Estados posibles
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

    # Campos de una publicación
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=280, blank=True, null=False, default="Sin descripción")
    imagen = models.ImageField()
    categoria = models.CharField(max_length=50, blank=False, null=False, choices=CATEGORIAS, default="Otros")
    estado = models.CharField(max_length=50, blank=False, null=False, choices=ESTADOS, default=ESTADOS[0][0])
    punto_encuentro = MultiSelectField(choices=PUNTOS_ENC, blank=True, max_length=100)
    dias_convenientes = MultiSelectField(choices=DIAS_SEMANA, blank=True, max_length=100)
    franja_horaria_inicio = models.TimeField(default=datetime.time(9,0,0)) # 9 AM
    franja_horaria_fin = models.TimeField(default=datetime.time(18,0,0)) # 6 PM
    franja_horaria = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=get_default_user)
    disponible_para_intercambio = models.BooleanField(default=True)
    
    FRANJA_HORARIA_REGEX = r'^entre las (\d{2}):(\d{2}) y las (\d{2}):(\d{2})$'

    def clean(self):
        """
        Valida la franja horaria seleccionada
        """
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

class EstadoIntercambio(ABC):
    # ABC indica clase abstracta
    @abstractmethod
    def aceptar(self, intercambio):
        pass

    @abstractmethod
    def rechazar(self, intercambio):
        pass

    @abstractmethod
    def cancelar(self, intercambio):
        pass

    @abstractmethod
    def obtener_estado(self):
        pass

class Aceptada(EstadoIntercambio):
    def aceptar(self, intercambio):
        raise ValueError("El intercambio ya está aceptado")

    def rechazar(self, intercambio):
        raise ValueError("No se puede rechazar un intercambio aceptado")

    def cancelar(self, intercambio):
        intercambio.estado = 'CANCELADA'
        intercambio.save()

    def obtener_estado(self):
        return "Aceptada"

class Rechazada(EstadoIntercambio):
    def aceptar(self, intercambio):
        raise ValueError("No se puede aceptar un intercambio rechazado")

    def rechazar(self, intercambio):
        raise ValueError("El intercambio ya está rechazado")
    
    def cancelar(self, intercambio):
        raise ValueError("No se puede cancelar un intercambio rechazado")
    
    def obtener_estado(self):
        return "Rechazada"
    
class Cancelada(EstadoIntercambio):
    def aceptar(self, intercambio):
        raise ValueError("No se puede aceptar un intercambio cancelado")

    def rechazar(self, intercambio):
        raise ValueError("No se puede rechazar un intercambio cancelado")
    
    def cancelar(self, intercambio):
        raise ValueError("El intercambio ya está cancelado")
    
    def obtener_estado(self):
        return "Cancelada"
    
class Pendiente(EstadoIntercambio):
    def aceptar(self, intercambio):
        intercambio.estado = 'ACEPTADA'
        intercambio.cancelar_ofertas_relacionadas()
        intercambio.save()

    def rechazar(self, intercambio):
        intercambio.estado = 'RECHAZADA'
        intercambio.save()

    def cancelar(self, intercambio):
        intercambio.estado = 'CANCELADA'
        intercambio.save()

    def obtener_estado(self):
        return "Pendiente"

class Intercambio(models.Model):

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
        ('CANCELADA', 'Cancelada'),
    ]

    publicacion_ofertante = models.ForeignKey('Publicacion', related_name='ofertas_realizadas', on_delete=models.CASCADE)
    publicacion_demandada = models.ForeignKey('Publicacion', related_name='ofertas_recibidas', on_delete=models.CASCADE)
    punto_encuentro = models.CharField(max_length=50, choices=Publicacion.PUNTOS_ENC) # 1 solo respecto de lo seleccionado en publicacion_demandada
    #dias_convenientes = MultiSelectField(choices=Publicacion.DIAS_SEMANA, blank=True, max_length=100) #N/A
    fecha_intercambio = models.DateField(default=datetime.datetime(2024,6,12)) # representa una fecha calendario sobre los días convenientes
    # La franja horaria debe representar 1 hora dentro del rango previamente seleccionado por el usuario
    #franja_horaria_inicio = models.TimeField(default=datetime.time(9,0,0))
    #franja_horaria_fin = models.TimeField(default=datetime.time(10,0,0))
    franja_horaria = models.TimeField(default=datetime.time(9,0,0))
    fecha_creacion = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    #aceptada = models.BooleanField(default=False)

    def __str__(self):
        return f"Intercambio de {self.publicacion_ofertante.nombre} por {self.publicacion_demandada.nombre}"

    def es_valida(self):
        return (self.publicacion_ofertante.categoria == self.publicacion_demandada.categoria and
                self.publicacion_ofertante.usuario != self.publicacion_demandada.usuario and
                not Intercambio.objects.filter(publicacion_demandada=self.publicacion_demandada, estado="ACEPTADA").exists())
        
    @property
    def estado_clase(self):
        estados = {
            'ACEPTADA': Aceptada(),
            'RECHAZADA': Rechazada(),
            'CANCELADA': Cancelada(),
            'PENDIENTE': Pendiente(),
        }
        return estados.get(self.estado)

    def aceptar(self):
        self.estado_clase.aceptar(self)

    def rechazar(self):
        self.estado_clase.rechazar(self)

    def cancelar(self):
        self.estado_clase.cancelar(self)

    def cancelar_ofertas_relacionadas(self):
        ofertas_relacionadas = Intercambio.objects.filter(
            publicacion_ofertante=self.publicacion_ofertante,
            estado='PENDIENTE'
        )
        for oferta in ofertas_relacionadas:
            if oferta != self:  
                oferta.cancelar()