from django import forms
from django.forms import inlineformset_factory
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo


class TipoEquipoForm(forms.ModelForm):
    class Meta: 
        model = TipoEquipo
        fields = ['prefixeq','tipoeq']
        labels = {
            'prefixeq': 'Prefijo',
            'tipoeq': 'Tipo equipo',
        }
        widgets = {
            'prefixeq': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese prefijo'
            }),
            'tipoeq': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese tipo equipo'
            })
        }

    def clean_prefixeq(self):
        prefixeq = self.cleaned_data.get('prefixeq')
        if TipoEquipo.objects.filter(prefixeq=prefixeq).exists():
            raise forms.ValidationError("El prefijo ya existe.")
        return prefixeq

class MarcaEquipoForm(forms.ModelForm):
    tipoeq = forms.ModelChoiceField(
            queryset=TipoEquipo.objects.all(),
            empty_label= "Seleccione un tipo de equipo",
            required=True,
            label="Tipos de equipo",
            widget= forms.Select({
                'class':'form-control',
                'placeholder':'Seleccione un tipo de equipo'
            })
        )
    class Meta:
        model = MarcaEquipo
        fields = ['marcaeq']
        labels = {
            'marcaeq': 'Marca'
        }
        widgets = {
            'marcaeq': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese marca'
            }),
        }
