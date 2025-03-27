from django.http import JsonResponse
from django.urls import  reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoEquipo, MarcaEquipo
from .forms import TipoEquipoForm, MarcaEquipoForm
# Create your views here.

# Vistas de tipos de equipos (CRUD)
class TipoEquipoListView(CreateView, ListView):
    model = TipoEquipo
    form_class = TipoEquipoForm
    template_name = 'tipoequipolist.html'
    context_object_name = 'equipos'
    success_url = reverse_lazy('tipoequipo_list')

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
    success_url = reverse_lazy('tipoequipo_list')

    def post(self, request, *args, **kwargs):
        equipo = get_object_or_404(TipoEquipo, pk=kwargs['pk'])
        equipo.prefixeq = equipo.prefixeq
        equipo.tipoeq = request.POST.get('tipoeq')
        equipo.save()
        return JsonResponse({'success': True})

class TipoEquipoDeleteView(DeleteView):
    model = TipoEquipo
    success_url = reverse_lazy('tipoequipo_list')

    def post(self, request, *args, **kwargs):
        equipo = get_object_or_404(TipoEquipo, pk=kwargs['pk'])
        equipo.delete()
        return JsonResponse({'success': True})

#Vistas para las marcas
class MarcaEquipoListView(CreateView, ListView):
    model = MarcaEquipo
    form_class = MarcaEquipoForm
    template_name = 'marcaequipolist.html'
    context_object_name = 'marcas'
    success_url = reverse_lazy('marcaequipo_list')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
class MarcaEquipoUpdateView(UpdateView):
    model = MarcaEquipo
    form_class = MarcaEquipoForm
    success_url = reverse_lazy('marcaequipo_list')

    def post(self, request, *args, **kwargs):
        marca = get_object_or_404(MarcaEquipo, pk=kwargs['pk'])
        marca.marcaeq = request.POST.get('marcaeq')
        tipos_equipos = request.POST.getlist('tipoeq')
        marca.tipoeq.set(tipos_equipos)
        marca.save()
        return JsonResponse({'success': True})

class MarcaEquipoDeleteView(DeleteView):
    model = MarcaEquipo
    success_url = reverse_lazy('marcaequipo_list')

    def post(self, request, *args, **kwargs):
        marca = get_object_or_404(MarcaEquipo, pk=kwargs['pk'])
        marca.delete()
        return JsonResponse({'success': True})