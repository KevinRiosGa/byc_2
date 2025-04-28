from django.db import models

# Create your models here.

class UnidadMedida(models.Model):
    codigo = models.CharField(max_length=3, unique=True, blank=False, null=False)
    nombre = models.CharField(max_length=255, blank=False, null=False)

class Region(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False)

class Comuna(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)    

class Empresa(models.Model):
    rut = models.CharField(max_length=8, unique=True, blank=False, null=False)
    dv = models.CharField(max_length=1, blank=False, null=False)
    razonSocial = models.CharField(max_length=255, blank=False, null=False)
    nombreFantasia = models.CharField(max_length=255)
    giro = models.CharField(max_length=255, blank=False, null=False)
    direccion = models.CharField(max_length=255, blank=False, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

class Proveedor(models.Model):
    rut = models.CharField(max_length=8, unique=True, blank=False, null=False)
    dv = models.CharField(max_length=1, blank=False, null=False)
    razonSocial = models.CharField(max_length=255, blank=False, null=False)
    nombreFantasia = models.CharField(max_length=255)
    giro = models.CharField(max_length=255, blank=False, null=False)
    direccion = models.CharField(max_length=255, blank=False, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)    

