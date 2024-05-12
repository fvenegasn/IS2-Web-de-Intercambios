from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['nombre', 'categoria', 'descripcion', 'imagen', 'estado', 'punto_encuentro']
