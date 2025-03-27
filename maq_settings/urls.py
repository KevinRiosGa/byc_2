from django.urls import path
from .views import (TipoEquipoListView, TipoEquipoUpdateView, TipoEquipoDeleteView, 
                    MarcaEquipoListView, MarcaEquipoUpdateView, MarcaEquipoDeleteView)

urlpatterns = [
    path('tipoequipo/', TipoEquipoListView.as_view(), name='tipoequipo_list'),
    path('tipoequipo/<int:pk>/editar/', TipoEquipoUpdateView.as_view(), name="tipoequipo_update"),
    path('tipoequipo/<int:pk>/eliminar/', TipoEquipoDeleteView.as_view(), name='tipoequipo_delete'),
    path('marcaequipo/', MarcaEquipoListView.as_view(), name='marcaequipo_list'),
    path('marcaequipo/<int:pk>/editar/', MarcaEquipoUpdateView.as_view(), name="marcaequipo_update"),
    path('marcaequipo/<int:pk>/eliminar/', MarcaEquipoDeleteView.as_view(), name='marcaequipo_delete'),
]