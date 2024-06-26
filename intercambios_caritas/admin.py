from django.contrib import admin
from .models import Publicacion, Usuario, Intercambio, Categoria, Filial

admin.site.register(Usuario)  # Registra el modelo de Usuario personalizado en el panel de administración
admin.site.register(Publicacion)  # Registra el modelo de Publicacion en el panel de administración
admin.site.register(Intercambio) # Registra el modelo de Intercambio en el panel de administración
admin.site.register(Categoria) # Registra el modelo de Categoria en el panel de administración
admin.site.register(Filial) # Registra el modelo de Filial en el panel de administración