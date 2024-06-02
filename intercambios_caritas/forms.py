from django import forms
from .models import Publicacion, Intercambio

class PublicacionForm(forms.ModelForm):
    dias_convenientes = forms.MultipleChoiceField(
        choices=Publicacion.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    franja_horaria_inicio = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=False,
        label='Franja horaria inicio'
    )
    franja_horaria_fin = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM'}),
        required=False,
        label='Franja horaria fin'
    )

    class Meta:
        model = Publicacion
        fields = ['nombre', 'descripcion', 'imagen', 'categoria', 'estado', 'punto_encuentro', 'dias_convenientes', 'franja_horaria_inicio', 'franja_horaria_fin']
        widgets = {
            'dias_convenientes': forms.CheckboxSelectMultiple,
            'franja_horaria_inicio': forms.TimeInput(format='%H:%M'),
            'franja_horaria_fin': forms.TimeInput(format='%H:%M'),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        franja_horaria_inicio = cleaned_data.get("franja_horaria_inicio")
        franja_horaria_fin = cleaned_data.get("franja_horaria_fin")

        if franja_horaria_inicio and franja_horaria_fin:
            if franja_horaria_inicio >= franja_horaria_fin:
                raise forms.ValidationError("La hora de inicio debe ser antes que la hora de finalización.")
        elif franja_horaria_inicio or franja_horaria_fin:
            raise forms.ValidationError("Debe especificar tanto la hora de inicio como la de finalización.")

        return cleaned_data

class IntercambioForm(forms.ModelForm):
    publicacion_ofertante = forms.ModelChoiceField(queryset=Publicacion.objects.none())

    class Meta:
        model = Intercambio
        fields = ['publicacion_ofertante', 'centro_encuentro', 'dias_convenientes', 'franja_horaria_inicio', 'franja_horaria_fin']
        widgets = {
            'dias_convenientes': forms.CheckboxSelectMultiple,
            'franja_horaria_inicio': forms.TimeInput(format='%H:%M'),
            'franja_horaria_fin': forms.TimeInput(format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(IntercambioForm, self).__init__(*args, **kwargs)
        self.fields['publicacion_ofertante'].queryset = Publicacion.objects.filter(usuario=user)