from django import forms
from .models import *



class PersonalCreationForm(forms.ModelForm):

    class Meta:
        model = Personal
        fields = ['rut', 'dvrut', 'nombre', 'apepat', 'apemat', 'sexo_id', 'fechanac', 'estcivil_id', 'correo', 'region_id', 'comuna_id', 'direccion']
        widgets = {
            'fechanac' : forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apepat': 'Apellido paterno',
            'apemat': 'Apellido Materno',
            'rut': 'Rut',
            'dvrut': 'Digito verificador',
            'fechanac': 'Fecha de nacimiento',
            'estcivil_id': 'Estado civil',
            'correo': 'Correo electrónico',
            'region_id': 'Región',
            'comuna_id': 'Comuna',
            'direccion': 'Dirección',
            'sexo_id':'Sexo',

        }
    sexo_id = forms.ModelChoiceField(queryset=Sexo.objects.all(), empty_label= '-----------')
    region_id = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label='-----------')
    comuna_id = forms.ModelChoiceField(queryset=Comuna.objects.all(), empty_label='-----------')
    estcivil_id = forms.ModelChoiceField(queryset=EstadoCivil.objects.all(), empty_label='-----------')


    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['rut'].widget.attrs.update({'id': 'id_rut'})
       self.fields['dvrut'].widget.attrs.update({'id': 'id_dvrut'})
       self.fields['dvrut'].widget.attrs.update({'readonly': 'readonly'})


class InfoLaboralPersonalForm(forms.ModelForm):

    class Meta:
        model = InfoLaboral
        fields = ['empresa_id', 'depto_id', 'cargo_id', 'fechacontrata']
        widgets = {
            'fechacontrata' : forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {'fechacontrata' : 'Fecha Contrata'}

    empresa_id = forms.ModelChoiceField(queryset=Empresa.objects.all(), empty_label='-----------')
    depto_id = forms.ModelChoiceField(queryset=DeptoEmpresa.objects.all(),empty_label='-----------')
    cargo_id = forms.ModelChoiceField(queryset=Cargo.objects.all(),empty_label='-----------')
