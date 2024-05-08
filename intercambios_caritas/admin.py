from django.contrib import admin
from .models import Usuario  # Importa el modelo de usuario personalizado

admin.site.register(Usuario)  # Registra el modelo de usuario personalizado en el panel de administración
