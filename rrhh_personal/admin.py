from django.contrib import admin
from .models import Personal, Region, Sexo, Comuna, EstadoCivil, InfoLaboral, Cargo, DeptoEmpresa, Empresa, Ausentismo, TipoAusentismo, Proveedor, TipoClasificacion, ClasificacionProveedor, TipoExamen, ResultadoExamen, Examen, TipoCertificacion, Certificacion, TipoLicencia, ClaseLicencia, LicenciaPorPersonal


# Register your models here.

admin.site.register(Region)
admin.site.register(Sexo)
admin.site.register(Comuna)
admin.site.register(EstadoCivil)
admin.site.register(Personal)
admin.site.register(InfoLaboral)
admin.site.register(Cargo)
admin.site.register(DeptoEmpresa)
admin.site.register(Ausentismo)
admin.site.register(TipoAusentismo)
admin.site.register(Proveedor)
admin.site.register(TipoClasificacion)
admin.site.register(ClasificacionProveedor)
admin.site.register(TipoExamen)
admin.site.register(ResultadoExamen)
admin.site.register(Examen)
admin.site.register(TipoCertificacion)
admin.site.register(Certificacion)
admin.site.register(TipoLicencia)
admin.site.register(ClaseLicencia)
admin.site.register(LicenciaPorPersonal)





@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    # Definir los campos que se mostrarán en el formulario
    fields = ('region_id', 'comuna_id', 'rut', 'dvRut', 'razonSocial', 'nombreFant', 'giro', 'direccion', 'telefono')
    list_display = ('empresa_id', 'razonSocial', 'rut', 'telefono')
    search_fields = ('razonSocial', 'rut', 'nombreFant', 'direccion')
