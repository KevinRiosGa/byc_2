from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,  get_object_or_404
from .forms import PersonalCreationForm, InfoLaboralPersonalForm
from django.shortcuts import redirect
from .models import Personal, InfoLaboral, Ausentismo, TipoAusentismo
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
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

        return render(request, self.template_name, {
            'form': form,
            'laboral_form': laboral_form
        })

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

        return render(request, self.template_name, {
            'form': form,
            'laboral_form': laboral_form
        })

    @staticmethod
    def _disable_form_fields(form):
        """Deshabilita todos los campos de un formulario."""
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'

#visualizar detalles del personal
class UserDetailView(LoginRequiredMixin, View):
    template_name = 'personal/view_personal.html'

    def get(self, request, pk, *args, **kwargs):
        #obtener usuario y su informacion
        usuario = get_object_or_404(Personal, personal_id=pk)
        info_laboral = usuario.infolaboral_set.first()
        context = {'usuario': usuario, 'info_laboral': info_laboral}

        return render(request, self.template_name, context)
