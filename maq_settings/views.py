from django.http import JsonResponse
from django.urls import  reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo
from .forms import TipoEquipoForm, MarcaEquipoForm, ModeloEquipoForm
# Create your views here.

# Vistas de tipos de equipos (CRUD)
class TipoEquipoListView(CreateView, ListView):
    model = TipoEquipo
    form_class = TipoEquipoForm
    template_name = 'tipoequipolist.html'
    context_object_name = 'equipos'
    success_url = reverse_lazy('tipoequipo_create')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class TipoEquipoUpdateView(UpdateView):
    model = TipoEquipo
    form_class = TipoEquipoForm
    success_url = reverse_lazy('tipoequipo_create')

    def post(self, request, *args, **kwargs):
        equipo = get_object_or_404(TipoEquipo, pk=kwargs['pk'])
        equipo.prefixeq = equipo.prefixeq
        equipo.tipoeq = request.POST.get('tipoeq')
        equipo.save()
        return JsonResponse({'success': True})

class TipoEquipoDeleteView(DeleteView):
    model = TipoEquipo
    success_url = reverse_lazy('tipoequipo_create')

    def post(self, request, *args, **kwargs):
        equipo = get_object_or_404(TipoEquipo, pk=kwargs['pk'])
        equipo.delete()
        return JsonResponse({'success': True})

#Vistas para las marcas
class MarcaEquipoCreateView(CreateView,ListView):
    model = MarcaEquipo
    form_class = MarcaEquipoForm
    template_name = 'marcaequipolist.html'
    context_object_name = 'marcas'
    success_url = reverse_lazy('marcaequipo_create')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class ObtenerDatosMarcaView(View):
    def get(self, request, pk):
        marca = MarcaEquipo.objects.get(pk=pk)
        tipos_equipos_ids = marca.tipoeq.values_list('id', flat=True)
        tipos_equipos = TipoEquipo.objects.filter(id__in=tipos_equipos_ids)  # Filtrar los tipos de equipos asociados
        tipos_equipos_data = [{'id': tipo.id, 'nombre': tipo.tipoeq} for tipo in tipos_equipos]

        return JsonResponse({
            'marca': marca.marcaeq,
            'tipos_equipos_ids': list(tipos_equipos_ids),  # IDs de los tipos de equipos seleccionados
            'tipos_equipos': tipos_equipos_data  # Datos completos de los tipos de equipos
        })

class MarcaEquipoUpdateView(UpdateView):
    model = MarcaEquipo
    form_class = MarcaEquipoForm
    template_name = 'marcaequipolist.html'
    context_object_name = 'marca'
    success_url = reverse_lazy('marcaequipo_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipoeqlist'] = TipoEquipo.objects.all()
        return context

    def form_valid(self, form):
        try:
            # Guardar los datos básicos de la marca
            self.object = form.save()
            
            # Actualizar los tipos de equipos
            self.object.tipoeq.clear()
            tipos_equipos = form.cleaned_data.get('tipoeq', [])
            if tipos_equipos:
                self.object.tipoeq.add(*tipos_equipos)
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class MarcaEquipoDeleteView(DeleteView):
    model = MarcaEquipo
    success_url = reverse_lazy('marcaequipo_create')

    def post(self, request, *args, **kwargs):
        marca = get_object_or_404(MarcaEquipo, pk=kwargs['pk'])
        marca.delete()
        return JsonResponse({'success': True})

class ModeloEquipoCreateView(CreateView, ListView):
    model = ModeloEquipo
    form_class = ModeloEquipoForm
    template_name = 'modeloequipolist.html'
    context_object_name = 'modelos'
    success_url = reverse_lazy('modeloequipo_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_equipos'] = TipoEquipo.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class ModeloEquipoUpdateView(UpdateView):
    model = ModeloEquipo
    form_class = ModeloEquipoForm
    success_url = reverse_lazy('modeloequipo_create')

    def post(self, request, *args, **kwargs):
        modelo = get_object_or_404(ModeloEquipo, pk=kwargs['pk'])
        form = self.get_form()
        if form.is_valid():
            modelo.tipoeq = form.cleaned_data['tipoeq']
            modelo.marcaeq = form.cleaned_data['marcaeq']
            modelo.modeloeq = form.cleaned_data['modeloeq']
            modelo.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class ModeloEquipoDeleteView(DeleteView):
    model = ModeloEquipo
    success_url = reverse_lazy('modeloequipo_create')

    def post(self, request, *args, **kwargs):
        modelo = get_object_or_404(ModeloEquipo, pk=kwargs['pk'])
        modelo.delete()
        return JsonResponse({'success': True})

class ObtenerMarcasPorTipoView(View):
    def get(self, request, tipo_id):
        marcas = MarcaEquipo.objects.filter(tipoeq__id=tipo_id)
        marcas_data = [{'id': marca.id, 'nombre': marca.marcaeq} for marca in marcas]
        return JsonResponse({'marcas': marcas_data})
    
