from django.contrib import admin
from .models import Publicacion, Usuario  # Importa el modelo de usuario personalizado

admin.site.register(Usuario)  # Registra el modelo de usuario personalizado en el panel de administración
admin.site.register(Publicacion)  # Registra el modelo de usuario personalizado en el panel de administración
