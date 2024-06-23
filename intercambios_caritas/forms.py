import datetime
from django.utils import timezone
from django import forms
from .models import Publicacion, Intercambio, Categoria

class PublicacionForm(forms.ModelForm):
    dias_convenientes = forms.MultipleChoiceField(
        choices=Publicacion.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    punto_encuentro = forms.MultipleChoiceField(
        choices=Publicacion.PUNTOS_ENC,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    franja_horaria_inicio = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=True,
        label='Franja horaria inicio'
    )
    franja_horaria_fin = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=True,
        label='Franja horaria fin'
    )
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label="-- Seleccione --")

    class Meta:
        model = Publicacion
        fields = ['nombre', 'descripcion', 'imagen', 'categoria', 'estado', 'punto_encuentro', 'dias_convenientes', 'franja_horaria_inicio', 'franja_horaria_fin']
        widgets = {
            'dias_convenientes': forms.CheckboxSelectMultiple,
            'punto_encuentro': forms.CheckboxSelectMultiple,
            'franja_horaria_inicio': forms.TimeInput(format='%H:%M'),
            'franja_horaria_fin': forms.TimeInput(format='%H:%M'),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        franja_horaria_inicio = cleaned_data.get("franja_horaria_inicio")
        franja_horaria_fin = cleaned_data.get("franja_horaria_fin")

        if franja_horaria_inicio and franja_horaria_fin:
            if franja_horaria_inicio >= franja_horaria_fin:
                self.add_error('franja_horaria_inicio', "La hora de inicio debe ser antes que la hora de finalización.")
                self.add_error('franja_horaria_fin', "La hora de inicio debe ser antes que la hora de finalización.")
                raise forms.ValidationError("La hora de inicio debe ser antes que la hora de finalización.")
        elif franja_horaria_inicio or franja_horaria_fin:
            self.add_error('franja_horaria_inicio', "Debe especificar tanto la hora de inicio como la de finalización.")
            self.add_error('franja_horaria_fin', "Debe especificar tanto la hora de inicio como la de finalización.")
            raise forms.ValidationError("Debe especificar tanto la hora de inicio como la de finalización.")

        return cleaned_data

class IntercambioForm(forms.ModelForm):
    publicacion_ofertante = forms.ModelChoiceField(queryset=Publicacion.objects.none())
    fecha_intercambio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    franja_horaria = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=True, # NO TOCAR
        label='Franja horaria'
    )

    class Meta:
        model = Intercambio
        fields = ['publicacion_ofertante', 'punto_encuentro', 'fecha_intercambio', 'franja_horaria']
        widgets = {
            'franja_horaria': forms.TimeInput(format='%H:%M')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        dias = kwargs.pop('dias')
        puntos = kwargs.pop('puntos')
        categoria = kwargs.pop('categoria')
        franja_horaria_inicio = kwargs.pop('franja_horaria_inicio')
        franja_horaria_fin = kwargs.pop('franja_horaria_fin')
        super(IntercambioForm, self).__init__(*args, **kwargs)
        self.fields['publicacion_ofertante'].queryset = Publicacion.objects.filter(usuario=user, categoria=categoria, disponible_para_intercambio=True)
        # self.fields['dias_convenientes'].choices = [(dia, dia) for dia in dias]

        self.fields['punto_encuentro'].choices = [(p, p) for p in puntos]

        self.franja_horaria_inicio_publicacion = franja_horaria_inicio
        self.franja_horaria_fin_publicacion = franja_horaria_fin

        self.fields['fecha_intercambio'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
        self.dias_disponibles = dias

    def clean_fecha_intercambio(self):
        fecha_intercambio = self.cleaned_data.get('fecha_intercambio')
        dias_convenientes = self.dias_disponibles

        if fecha_intercambio and (datetime.datetime.combine(fecha_intercambio,datetime.time(0,0)) < datetime.datetime.now()):
            raise forms.ValidationError("La fecha del intercambio no puede ser anterior a hoy.")

        # Diccionario de traducción de días de la semana
        dias_espanol = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }

        # Obtener el nombre del día en español
        dia_semana = fecha_intercambio.strftime('%A')
        dia_semana_espanol = dias_espanol.get(dia_semana)

        # Verificar si el día de la semana está en la lista de días convenientes
        if fecha_intercambio and dia_semana_espanol not in dias_convenientes:
            raise forms.ValidationError(f"La fecha seleccionada debe ser un {', '.join(dias_convenientes)}.")
        return fecha_intercambio
        

    def clean(self):
        cleaned_data = super().clean()
        franja_horaria = cleaned_data.get("franja_horaria")

        if franja_horaria:
            if not (self.franja_horaria_inicio_publicacion <= franja_horaria <= self.franja_horaria_fin_publicacion):
                raise forms.ValidationError(f"La hora debe estar dentro del rango {self.franja_horaria_inicio_publicacion} y {self.franja_horaria_fin_publicacion}.")
        else:
            raise forms.ValidationError("Debe especificar la hora del intercambio.")

        return cleaned_data
    
from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion']



class UpdatePublicacionForm(forms.ModelForm):
    dias_convenientes = forms.MultipleChoiceField(
        choices=Publicacion.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    punto_encuentro = forms.MultipleChoiceField(
        choices=Publicacion.PUNTOS_ENC,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    franja_horaria_inicio = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=True,
        label='Franja horaria inicio'
    )
    franja_horaria_fin = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=True,
        label='Franja horaria fin'
    )

    class Meta:
        model = Publicacion
        fields = ['nombre', 'descripcion', 'imagen', 'categoria', 'estado', 'punto_encuentro', 'dias_convenientes', 'franja_horaria_inicio', 'franja_horaria_fin']
        widgets = {
            'dias_convenientes': forms.CheckboxSelectMultiple,
            'punto_encuentro': forms.CheckboxSelectMultiple,
            'franja_horaria_inicio': forms.TimeInput(format='%H:%M'),
            'franja_horaria_fin': forms.TimeInput(format='%H:%M'),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        capitalized_nombre = nombre.title() 
        if Categoria.objects.filter(nombre__iexact=capitalized_nombre).exists():
            raise forms.ValidationError("")
        return capitalized_nombre