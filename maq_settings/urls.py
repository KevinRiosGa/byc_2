from django.urls import path
from .views import (TipoEquipoListView, TipoEquipoUpdateView, TipoEquipoDeleteView, 
                    MarcaEquipoCreateView, MarcaEquipoUpdateView, ObtenerDatosMarcaView,
                    ModeloEquipoCreateView, ModeloEquipoUpdateView, ModeloEquipoDeleteView,
                    ObtenerMarcasPorTipoView)

urlpatterns = [
    path('tipoequipo/', TipoEquipoListView.as_view(), name='tipoequipo_list'),
    path('tipoequipo/<int:pk>/editar/', TipoEquipoUpdateView.as_view(), name="tipoequipo_update"),
    path('tipoequipo/<int:pk>/eliminar/', TipoEquipoDeleteView.as_view(), name='tipoequipo_delete'),
    path('marcaequipo/', MarcaEquipoCreateView.as_view(), name='marcaequipo_create'),
    path('editar_marca/<int:pk>/', MarcaEquipoUpdateView.as_view(), name='editar_marca'),
    path('modeloequipo/', ModeloEquipoCreateView.as_view(), name='modeloequipo_create'),
    path('modeloequipo/<int:pk>/editar/', ModeloEquipoUpdateView.as_view(), name='modeloequipo_update'),
    path('modeloequipo/<int:pk>/eliminar/', ModeloEquipoDeleteView.as_view(), name='modeloequipo_delete'),
    #Obtención de datos mediante AJAX
    path('obtener_datos_marca/<int:pk>/', ObtenerDatosMarcaView.as_view(), name='obtener_datos_marca'),
    path('obtener_marcas_por_tipo/<int:tipo_id>/', ObtenerMarcasPorTipoView.as_view(), name='obtener_marcas_por_tipo'),
]