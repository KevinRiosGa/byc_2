from django.db import models



# Create your models here.
class Sexo(models.Model):
    sexo_id = models.AutoField(primary_key=True, null=False, blank=False)
    sexo = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.sexo
    
    class Meta:
        db_table = 'sexo'

class EstadoCivil(models.Model):
    estcivil_id = models.AutoField(primary_key=True, null=False, blank=False)
    estadocivil = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.estadocivil
    
    class Meta:
        db_table = 'estadocivil'

class Region(models.Model):
    region_id = models.AutoField(primary_key=True, null=False, blank=False)
    region = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.region
    
    class Meta:
        db_table = 'region'

class Comuna(models.Model):
    comuna_id = models.AutoField(primary_key=True, null=False, blank=False)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id')
    comuna = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.comuna
    
    class Meta:
        db_table = 'comuna'

class Personal(models.Model):
    personal_id = models.AutoField(primary_key=True, null=False, blank=False)
    sexo_id = models.ForeignKey(Sexo, on_delete=models.CASCADE, db_column='sexo_id', null=True, blank=True)
    estcivil_id = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE, db_column='estcivil_id', null=True, blank=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id', null=True, blank=True)
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE, db_column='comuna_id', null=True, blank=True)
    rut = models.CharField(max_length=8, null=False, blank=False, unique=True)
    dvrut = models.CharField(max_length=1, null=False, blank= False)
    nombre = models.CharField(max_length=100, null=False, blank= False)
    apepat = models.CharField(max_length=50, null=False, blank= False)
    apemat = models.CharField(max_length=50)
    fechanac = models.DateField(null=True, blank=True)
    correo = models.CharField(max_length=100, null=False, blank=False, unique=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nombre + " " + self.apepat + " " + self.apemat
    
    class Meta:
        db_table = 'Personal'

    def save(self, *args, **kwargs):

        
        self.rut = self.rut.upper()
        self.dvrut = self.dvrut.upper()
        self.nombre = self.nombre.upper()
        self.apepat = self.apepat.upper()
        self.apemat = self.apemat.upper()
        self.correo = self.correo.upper()
        self.direccion = self.direccion.upper()
        super().save(*args, *kwargs)


class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True, null=False, blank=False)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE, db_column='region_id', null=True, blank=True, verbose_name='Región')
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE, db_column='comuna_id', null=True, blank=True, verbose_name='Comuna')
    rut = models.CharField(max_length=8, null=False, blank=False, unique=True, db_column='rut', verbose_name='Rut')
    dvRut = models.CharField(max_length=1, blank=False, null=False, db_column='dvRut', verbose_name='Digito Verificador')
    razonSocial = models.CharField(max_length=100, null=False, blank=False, db_column='razonSocial', verbose_name='Razón Social')
    nombreFant = models.CharField(max_length=100, null=True, blank=True, db_column='nombreFant', verbose_name='Nombre de fantasía')
    giro = models.CharField(max_length=150, null=False, blank=False, db_column='giro', verbose_name='Giro')
    direccion = models.CharField(max_length=150, blank=False, null=False, db_column='direccion', verbose_name='Dirección')
    telefono = models.CharField(max_length=11, blank=True, null=True, verbose_name='Teléfono')

    def save(self, *args, **kwargs):
        # Convertir a mayúsculas los campos deseados
        self.rut = self.rut.upper()
        self.dvRut = self.dvRut.upper()
        self.razonSocial = self.razonSocial.upper()
        self.nombreFant = self.nombreFant.upper() if self.nombreFant else None
        self.giro = self.giro.upper()
        self.direccion = self.direccion.upper()
        super().save(*args, **kwargs)  # Llamar al método save original

    def __str__(self):
        return self.razonSocial


class DeptoEmpresa(models.Model):
    depto_id = models.AutoField(primary_key=True, blank=False, null=False)
    depto = models.CharField(max_length=50, db_column='depto', blank=False, null=False)

    def __str__(self):
        return self.depto


class Cargo(models.Model):
    cargo_id = models.AutoField(primary_key=True, blank=False, null=False)
    depto_id = models.ForeignKey(DeptoEmpresa, on_delete=models.CASCADE, db_column='depto_id', blank=False, null=False)
    cargo = models.CharField(max_length=50, db_column='cargo', blank=False, null=False)

    def __str__(self):
        return self.cargo


class InfoLaboral(models.Model):
    infolab_id = models.AutoField(primary_key=True, null=False, blank=False)
    personal_id = models.ForeignKey(Personal, on_delete=models.CASCADE, db_column='personal_id', null=False, blank=False)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='empresa_id', null=False, blank=False)
    depto_id = models.ForeignKey(DeptoEmpresa, on_delete=models.CASCADE, db_column='depto_id', null=False, blank=False)
    cargo_id = models.ForeignKey(Cargo, on_delete=models.CASCADE, db_column='cargo_id',blank=False, null=False)
    fechacontrata = models.DateField(blank=False, null=False)


class TipoAusentismo(models.Model):
    tipoausen_id = models.AutoField(primary_key=True, null=False, blank=False)
    tipo = models.CharField(max_length=100, null=False, blank=False, db_column='tipo' )

    def __str__(self):
        return self.tipo


class Ausentismo(models.Model):
    ausentismo_id = models.AutoField(primary_key=True, null=False, blank=False)
    tipoausen_id = models.ForeignKey(TipoAusentismo, on_delete=models.CASCADE, db_column='tipoausen_id', null=False, blank=False)
    personal_id = models.ForeignKey(Personal, on_delete=models.CASCADE, db_column='personal_id', null=False, blank=False)
    fechaini = models.DateField(null=False, blank=False)
    fechafin = models.DateField(null=False, blank=False)
    observacion = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        trabajador = f"{self.personal_id.nombre} {self.personal_id.apepat} {self.personal_id.apemat}"
        return f"{self.tipoausen_id} - {trabajador} ({self.fechaini} a {self.fechafin})"
