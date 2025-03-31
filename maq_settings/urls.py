from django.urls import path
from .views import (TipoEquipoListView, TipoEquipoUpdateView, TipoEquipoDeleteView, 
                    MarcaEquipoCreateView,MarcaEquipoUpdateView,ObtenerDatosMarcaView)

urlpatterns = [
    path('tipoequipo/', TipoEquipoListView.as_view(), name='tipoequipo_list'),
    path('tipoequipo/<int:pk>/editar/', TipoEquipoUpdateView.as_view(), name="tipoequipo_update"),
    path('tipoequipo/<int:pk>/eliminar/', TipoEquipoDeleteView.as_view(), name='tipoequipo_delete'),
    path('marcaequipo/',MarcaEquipoCreateView.as_view(),name='marcaequipo_create'),
    path('editar_marca/<int:pk>/', MarcaEquipoUpdateView.as_view(), name='editar_marca'),
    # URLs de obtención de datos mediante AJAX
    path('obtener_datos_marca/<int:pk>/', ObtenerDatosMarcaView.as_view(), name='obtener_datos_marca'),
]