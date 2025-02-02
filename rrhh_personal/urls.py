from django.urls import path
from .views import *


urlpatterns = [
    #path para crear personal
    path('create_personal/', CreatePersonalView.as_view(), name='create_personal'),
    #path para mostrar la tabla del personal
    path('personal_table/', TablePersonalView.as_view(), name='table_personal'),
    #path para crear personal
    path('personal/<int:pk>/edit_personal', PersonalEditView.as_view(), name='edit_personal'),
    path('personal/<int:pk>/detail_personal', PersonalDetailView.as_view(), name='detail_personal'),
    path('personal/<int:pk>/edit_license', PersonalLicenceEditView.as_view(), name='personalLicenceEditView'),
    path('personal/<int:pk>/edit_certification', PersonalCertificationEditView.as_view(), name='personalCertificationEditView'),
    path('personal/<int:pk>/edit_examen', PersonalExamenEditView.as_view(), name='personalExamenEditView')
]