from django.contrib import admin
from .models import Publicacion, Usuario, Intercambio

admin.site.register(Usuario)  # Registra el modelo de Usuario personalizado en el panel de administración
admin.site.register(Publicacion)  # Registra el modelo de Publicacion personalizado en el panel de administración
admin.site.register(Intercambio) # Registra el modelo de Intercambio personalizado en el panel de administración
