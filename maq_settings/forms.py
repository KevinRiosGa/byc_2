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

class ModeloEquipoForm(forms.ModelForm):
    class Meta:
        model = ModeloEquipo
        fields = ['tipoeq', 'marcaeq', 'modeloeq']
        labels = {
            'tipoeq': 'Tipo equipo',
            'marcaeq': 'Marca',
            'modeloeq': 'Modelo'
        }
        widgets = {
            'tipoeq': forms.Select(attrs={
                'class': 'form-control',
                'id': 'tipo_equipo_select'
            }),
            'marcaeq': forms.Select(attrs={
                'class': 'form-control',
                'id': 'marca_equipo_select'
            }),
            'modeloeq': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese modelo'
            })
        }
        error_messages = {
            'modeloeq': {
                'unique': 'Este modelo ya existe para la marca y tipo seleccionados.'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        tipoeq = cleaned_data.get('tipoeq')
        marcaeq = cleaned_data.get('marcaeq')
        modeloeq = cleaned_data.get('modeloeq')

        if tipoeq and marcaeq and modeloeq:
            if ModeloEquipo.objects.filter(
                tipoeq=tipoeq,
                marcaeq=marcaeq,
                modeloeq=modeloeq
            ).exists():
                # Si estamos editando, excluir el modelo actual
                if self.instance.pk:
                    if not ModeloEquipo.objects.filter(
                        tipoeq=tipoeq,
                        marcaeq=marcaeq,
                        modeloeq=modeloeq
                    ).exclude(pk=self.instance.pk).exists():
                        return cleaned_data
                
        return cleaned_data  
         