from django.urls import path
from .views import (TipoEquipoListView, TipoEquipoUpdateView, TipoEquipoDeleteView, 
                    MarcaEquipoCreateView, MarcaEquipoUpdateView, ObtenerDatosMarcaView, MarcaEquipoDeleteView,
                    ModeloEquipoCreateView, ModeloEquipoUpdateView, ModeloEquipoDeleteView,
                    ObtenerMarcasPorTipoView, SeccionEspecificacionCreateView, EspecificacionCreateView,
                    SeccionEspecificacionUpdateView, SeccionEspecificacionDeleteView, EspecificacionUpdateView,
                    EspecificacionDeleteView)

urlpatterns = [
    path('tipoequipo/', TipoEquipoListView.as_view(), name='tipoequipo_create'),
    path('tipoequipo/<int:pk>/editar/', TipoEquipoUpdateView.as_view(), name='tipoequipo_update'),
    path('tipoequipo/<int:pk>/eliminar/', TipoEquipoDeleteView.as_view(), name='tipoequipo_delete'),
    path('marcaequipo/', MarcaEquipoCreateView.as_view(), name='marcaequipo_create'),
    path('marcaequipo/<int:pk>/editar/', MarcaEquipoUpdateView.as_view(), name='marcaequipo_update'),
    path('marcaequipo/<int:pk>/eliminar/', MarcaEquipoDeleteView.as_view(), name='marcaequipo_delete'),
    path('modeloequipo/', ModeloEquipoCreateView.as_view(), name='modeloequipo_create'),
    path('modeloequipo/<int:pk>/editar/', ModeloEquipoUpdateView.as_view(), name='modeloequipo_update'),
    path('modeloequipo/<int:pk>/eliminar/', ModeloEquipoDeleteView.as_view(), name='modeloequipo_delete'),
    path('seccionespecificacion/', SeccionEspecificacionCreateView.as_view(), name='seccionespecificacion_create'),
    path('seccionespecificacion/<int:pk>/editar/', SeccionEspecificacionUpdateView.as_view(), name='seccionespecificacion_update'),
    path('seccionespecificacion/<int:pk>/eliminar/', SeccionEspecificacionDeleteView.as_view(), name='seccionespecificacion_delete'),
    path('especificacion/', EspecificacionCreateView.as_view(), name='especificacion_create'),
    path('especificacion/<int:pk>/editar/', EspecificacionUpdateView.as_view(), name='especificacion_update'),
    path('especificacion/<int:pk>/eliminar/', EspecificacionDeleteView.as_view(), name='especificacion_delete'),
    #Obtención de datos mediante AJAX
    path('obtener_datos_marca/<int:pk>/', ObtenerDatosMarcaView.as_view(), name='obtener_datos_marca'),
    path('obtener_marcas_por_tipo/<int:tipo_id>/', ObtenerMarcasPorTipoView.as_view(), name='obtener_marcas_por_tipo'),
]