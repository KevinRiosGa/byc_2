from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,  get_object_or_404
from .forms import PersonalCreationForm, InfoLaboralPersonalForm, LicenciasPersonal, CertificacionPersonal, ExamenPersonal
from django.shortcuts import redirect
from .models import Personal, InfoLaboral, Ausentismo, TipoAusentismo, LicenciaPorPersonal, Certificacion, Examen
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from django.db.models import Max
# Create your views here.

#Vista para crear usuario
class CreatePersonalView(LoginRequiredMixin, View):
    template_name = 'personal/create_personal.html'
    
    def get(self, request, *args, **kwargs):
        personal_form = PersonalCreationForm()
        laboral_form = InfoLaboralPersonalForm()
        return render(request, self.template_name, {
            'personal_form': personal_form,
            'laboral_form': laboral_form,
        })

    def post(self, request, *args, **kwargs):
        personal_form = PersonalCreationForm(request.POST)
        laboral_form = InfoLaboralPersonalForm(request.POST)

        if personal_form.is_valid() and laboral_form.is_valid():
            try:
                with transaction.atomic():
                    personal = personal_form.save()
                    laboral_form.instance.personal_id = personal
                    laboral_form.save()
                    return redirect('table_personal')
            except Exception as e:
                print("Error al guardar:", e)
        else:
            print("Errores del formulario Personal:", personal_form.errors)
            print("Errores del formulario Laboral:", laboral_form.errors)

        return render(request, self.template_name, {
            'personal_form': personal_form,
            'laboral_form': laboral_form,
        })

#vista para tabla de personal
class TablePersonalView(LoginRequiredMixin, ListView):
    model = Personal
    template_name = 'personal/table_personal.html'
    context_object_name = 'personal'


#vista para editar al personal
class PersonalEditView(LoginRequiredMixin, View):
    template_name = 'personal/edit_personal.html'

    def get(self, request, pk, *args, **kwargs):
        # Obtener el usuario y su información laboral
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()

        # Inicializar los formularios con instancias
        form = PersonalCreationForm(instance=usuario)
        laboral_form = InfoLaboralPersonalForm(instance=info_laboral)

        # Deshabilitar campos de los formularios
        self._disable_form_fields(form)
        self._disable_form_fields(laboral_form)

        context = {'form': form, 'laboral_form': laboral_form}

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        # Obtener el usuario y su información laboral
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()

        # Inicializar los formularios con datos enviados
        form = PersonalCreationForm(request.POST, instance=usuario)
        laboral_form = InfoLaboralPersonalForm(request.POST, instance=info_laboral)

        if form.is_valid() and laboral_form.is_valid():
            form.save()
            laboral_form.save()
        
        context =  {'form': form,'laboral_form': laboral_form}

        return render(request, self.template_name, context)

    @staticmethod
    def _disable_form_fields(form):
        """Deshabilita todos los campos de un formulario."""
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'

#vista para visualizar detalles del personal
class PersonalDetailView(LoginRequiredMixin, View):
    template_name = 'personal/view_personal.html'

    def get(self, request, pk, *args, **kwargs):
        #obtener usuario y su informacion
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()
        context = {'usuario': usuario, 'info_laboral': info_laboral}

        return render(request, self.template_name, context)

#vista para ingresar licencias para el personal
class PersonalLicenceEditView(LoginRequiredMixin, View):
    #template_name = 'personal/LicenceEdit_personal.html'
    template_name = 'personal/view_personal.html'

    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()

        historial_licencias_completos = (
        LicenciaPorPersonal.objects.filter(personal_id=usuario).order_by('claseLicencia_id').distinct('claseLicencia_id')
        )

        form = LicenciasPersonal()
        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral, 'historial_licencias': historial_licencias_completos}

        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()
        form = LicenciasPersonal(request.POST, request.FILES)

        if form.is_valid():
            licencia = form.save(commit=False)
            licencia.personal_id = usuario
            LicenciaPorPersonal.objects.filter(personal_id=usuario, claseLicencia_id = licencia.claseLicencia_id).delete()
            licencia.save()
            return redirect('personalLicenceEditView', pk=pk)
        
        historial_licencias = LicenciaPorPersonal.objects.filter(personal_id=usuario)
        context = {
            'form': form,
            'usuario': usuario,
            'historial_licencias': historial_licencias,
            'info_laboral': info_laboral,
        }
        return render(request, self.template_name, context)
        

class PersonalCertificationEditView(LoginRequiredMixin, View):
    template_name = 'personal/CertificationEdit_personal.html'

    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()

        form = CertificacionPersonal()

        historial_de_certificaciones = Certificacion.objects.filter(personal_id=usuario)
        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral, 'historial_de_certificaciones': historial_de_certificaciones}


        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()
        form = CertificacionPersonal(request.POST, request.FILES)

        if form.is_valid():
            certificacion = form.save(commit=False)
            certificacion.personal_id = usuario
            certificacion.save()

            return redirect('personalCertificationEditView', pk=pk)
        
        context = {
            'form': form,
            'usuario': usuario,
            'info_laboral': info_laboral
        }
        return render(request, self.template_name, context)
    
class PersonalExamenEditView(LoginRequiredMixin, View):
    template_name = 'personal/ExamenEdit_personal.html'

    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()

        form = ExamenPersonal()

        historial_de_examen = Examen.objects.filter(personal_id=usuario)
        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral, 'historial_de_examen': historial_de_examen}


        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()
        form = ExamenPersonal(request.POST, request.FILES)

        if form.is_valid():
            certificacion = form.save(commit=False)
            certificacion.personal_id = usuario
            certificacion.save()

            return redirect('personalExamenEditView', pk=pk)
        
        context = {
            'form': form,
            'usuario': usuario,
            'info_laboral': info_laboral
        }
        return render(request, self.template_name, context)    
    


class PersonalEditView(LoginRequiredMixin, View):
    template_name = 'personal/view_personal.html'

    def _get_personal_data(self, pk):
        #Obtiene los datos del usuario y su información laboral
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()
        return usuario, info_laboral

    def personalDetailView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)
        context = {'usuario': usuario, 'info_laboral': info_laboral}
        return render(request, self.template_name, context)

    def personalEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form_edit_personal = PersonalCreationForm(instance=usuario)
        laboral_form_edit_personal = InfoLaboralPersonalForm(instance=info_laboral)

        # Deshabilitar campos
        self._disable_form_fields(form_edit_personal)
        self._disable_form_fields(laboral_form_edit_personal)

        context = {'form_edit_personal': form_edit_personal, 'laboral_form_edit_personal': laboral_form_edit_personal}
        return render(request, self.template_name, context)

    def personalLicenceEditView(self, request, pk, *args, **kwargs):
        print("Llegó al método personalLicenceEditView")
        usuario, info_laboral = self._get_personal_data(pk)

        historial_licencias_completos = LicenciaPorPersonal.objects.filter(personal_id=usuario).order_by('claseLicencia_id').distinct('claseLicencia_id')

        form_license = LicenciasPersonal()
        context = {'form_license': form_license, 'usuario': usuario, 'info_laboral': info_laboral, 'historial_licencias': historial_licencias_completos}
        return render(request, self.template_name, context)

    def personalCertificationEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form = CertificacionPersonal()
        historial_de_certificaciones = Certificacion.objects.filter(personal_id=usuario)

        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral, 'historial_de_certificaciones': historial_de_certificaciones}
        return render(request, self.template_name, context)

    def personalExamenEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form = ExamenPersonal()
        historial_de_examen = Examen.objects.filter(personal_id=usuario)

        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral, 'historial_de_examen': historial_de_examen}
        return render(request, self.template_name, context)

    def postPersonalEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form = PersonalCreationForm(request.POST, instance=usuario)
        laboral_form = InfoLaboralPersonalForm(request.POST, instance=info_laboral)

        if form.is_valid() and laboral_form.is_valid():
            form.save()
            laboral_form.save()

        context = {'form': form, 'laboral_form': laboral_form}
        return render(request, self.template_name, context)

    def postPersonalLicenceEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form = LicenciasPersonal(request.POST, request.FILES)
        if form.is_valid():
            licencia = form.save(commit=False)
            licencia.personal_id = usuario
            LicenciaPorPersonal.objects.filter(personal_id=usuario, claseLicencia_id=licencia.claseLicencia_id).delete()
            licencia.save()
            return redirect('personalLicenceEditView', pk=pk)

        historial_licencias = LicenciaPorPersonal.objects.filter(personal_id=usuario)
        context = {'form': form, 'usuario': usuario, 'historial_licencias': historial_licencias, 'info_laboral': info_laboral}
        return render(request, self.template_name, context)

    def postPersonalCertificationEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form = CertificacionPersonal(request.POST, request.FILES)
        if form.is_valid():
            certificacion = form.save(commit=False)
            certificacion.personal_id = usuario
            certificacion.save()
            return redirect('personalCertificationEditView', pk=pk)

        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral}
        return render(request, self.template_name, context)

    def postPersonalExamenEditView(self, request, pk, *args, **kwargs):
        usuario, info_laboral = self._get_personal_data(pk)

        form = ExamenPersonal(request.POST, request.FILES)
        if form.is_valid():
            examen = form.save(commit=False)
            examen.personal_id = usuario
            examen.save()
            return redirect('personalExamenEditView', pk=pk)

        context = {'form': form, 'usuario': usuario, 'info_laboral': info_laboral}
        return render(request, self.template_name, context)

    @staticmethod
    def _disable_form_fields(form):
        """Deshabilita todos los campos de un formulario."""
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
