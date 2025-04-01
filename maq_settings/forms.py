from django import forms
from django.forms import inlineformset_factory
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo
from django.core.exceptions import ValidationError

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
    tipoeq = forms.ModelMultipleChoiceField(
        queryset=TipoEquipo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Tipo equipo',
        required=True,
    )

    class Meta:
        model = MarcaEquipo
        fields = ['marcaeq', 'tipoeq']
        labels = {'marcaeq': 'Marca'}
        widgets = {
            'marcaeq': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese marca'
            })
        }

    def clean_marcaeq(self):
        marcaeq = self.cleaned_data.get('marcaeq')
        if not self.instance.pk and MarcaEquipo.objects.filter(marcaeq=marcaeq).exists():
            raise forms.ValidationError("La marca ya existe.")
        return marcaeq  
         