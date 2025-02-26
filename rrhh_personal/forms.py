from django import forms
from .models import *


#formulario para la creacion de personas
class PersonalCreationForm(forms.ModelForm):

    class Meta:
        model = Personal
        fields = ['rut', 'dvrut', 'nombre', 'apepat', 'apemat', 'sexo_id', 'fechanac', 'estcivil_id', 'correo', 'region_id', 'comuna_id', 'direccion']
        widgets = {
            'fechanac' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apepat': 'Apellido paterno',
            'apemat': 'Apellido Materno',
            'rut': 'Rut',
            'dvrut': 'Dígito verificador',
            'fechanac': 'Fecha de nacimiento',
            'estcivil_id': 'Estado civil',
            'correo': 'Correo electrónico',
            'region_id': 'Región',
            'comuna_id': 'Comuna',
            'direccion': 'Dirección',
            'sexo_id':'Sexo',
        }

    sexo_id = forms.ModelChoiceField(queryset=Sexo.objects.all(), empty_label= '-----------', widget=forms.Select(attrs={'class': 'form-select'}))
    region_id = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label='-----------', widget=forms.Select(attrs={'class': 'form-select'}))
    comuna_id = forms.ModelChoiceField(queryset=Comuna.objects.all(), empty_label='-----------', widget=forms.Select(attrs={'class': 'form-select'}))
    estcivil_id = forms.ModelChoiceField(queryset=EstadoCivil.objects.all(), empty_label='-----------', widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Actualizando los widgets para rut y dvrut
        self.fields['rut'].widget.attrs.update({'class': 'form-control', 'id': 'id_rut'})
        self.fields['dvrut'].widget.attrs.update({'class': 'form-control', 'id': 'id_dvrut', 'readonly': 'readonly'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['apepat'].widget.attrs.update({'class': 'form-control'})
        self.fields['apemat'].widget.attrs.update({'class': 'form-control'})

        # Personalización de campos select
        self.fields['sexo_id'].widget.attrs.update({'class': 'form-select', 'aria-label': 'Sexo'})
        self.fields['region_id'].widget.attrs.update({'class': 'form-select', 'aria-label': 'Región'})
        self.fields['comuna_id'].widget.attrs.update({'class': 'form-select', 'aria-label': 'Comuna'})
        self.fields['estcivil_id'].widget.attrs.update({'class': 'form-select', 'aria-label': 'Estado civil'})
        self.fields['fechanac'].widget.attrs.update({'class': 'form-control', 'aria-label': 'Fecha de nacimiento'})
        self.fields['correo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})

#formulario para ingresar la informacion laboral de las personas
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


#formularios de licencias --------------------------------------------------------------
class LicenciasPersonal(forms.ModelForm):
    class Meta:
        model = LicenciaPorPersonal
        fields = ['tipoLicencia_id', 'claseLicencia_id', 'fechaEmision', 'fechaVencimiento', 'rutaDoc','observacion']
        widgets = {
            'fechaEmision': forms.DateInput(attrs={'type': 'date'}),
            'fechaVencimiento': forms.DateInput(attrs={'type': 'date'}),
            'rutaDoc': forms.FileInput(attrs={'accept': 'application/pdf, image/jpg, image/png'})
        }
        labels = {'tipoLicencia_id': 'Tipo de licencia', 'claseLicencia_id': 'Clase de licencia', 'fechaEmision': 'Fecha de emisión', 'fechaVencimiento': 'Fecha de vencimiento', 'rutaDoc': 'Documento', 'observacion': 'Observación'}

        tipoLicencia_id = forms.ModelChoiceField(queryset=TipoLicencia.objects.all(), empty_label='-----------')
        claseLicencia_id = forms.ModelChoiceField(queryset=ClaseLicencia.objects.all(), empty_label='-----------')



#formulario para certificacion------------------------------------------------------------  
class CertificacionPersonal(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = ['proveedor_id', 'tipoCertificacion_id', 'fechaEmision', 'fechaVencimiento', 'rutaDoc', 'observacion']
        widgets = {
            'fechaEmision': forms.DateInput(attrs={'type': 'date'}),
            'fechaVencimiento': forms.DateInput(attrs={'type':'date'}),
            'rutaDoc': forms.FileInput(attrs={'accept': 'application/pdf, image/jpg, image/png'}),
        }

        labels = {'proveedor_id': 'Proveedor', 'tipoCertificacion_id': 'Tipo de certificación', 'fechaEmision': 'Fecha de emisión', 'fechaVencimiento': 'Fecha de vencimiento', 'rutaDoc': 'Documento', 'observacion': 'Observación'}

        proveedor_id = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label='-----------')
        tipoCertificacion_id = forms.ModelChoiceField(queryset=TipoCertificacion.objects.all(), empty_label='-----------')
        

#formulario para examenes
class ExamenPersonal(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['tipoEx_id','resultadoEx_id', 'proveedor_id','fechaEmision','fechaVencimiento', 'rutaDoc', 'observacion']
        widgets = {
            'fechaEmision' : forms.DateInput(attrs={'type':'date'}),
            'fechaVencimiento' : forms.DateInput(attrs={'type': 'date'}),
            'rutaDoc' : forms.FileInput(attrs={'accept': 'application/pdf, image/jpg, image/png'})
        }

        labels = {'tipoEx_id': 'Tipo de examen', 'resultadoEx_id': 'Resultado', 'proveedor_id': 'Proveedor', 'fechaEmision': 'Fecha de emisión', 'fechaVencimiento': 'Fecha de vencimiento', 'rutaDoc': 'Documento', 'observacion': 'Observación'}

        tipoEx_id = forms.ModelChoiceField(queryset=TipoExamen.objects.all(), empty_label='-----------')
        resultadoEx_id = forms.ModelChoiceField(queryset=ResultadoExamen.objects.all(), empty_label='-----------')
        proveedor_id = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label='-----------')

        