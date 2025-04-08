from django.db import models

# Create your models here.

class TipoEquipo(models.Model):
    prefixeq = models.CharField(max_length=2, unique=True, null=False, blank=False)
    tipoeq = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.tipoeq}"

    class Meta:
        ordering = ['tipoeq']
        verbose_name = 'Tipo equipo'
        verbose_name_plural = 'Tipo equipos'

class MarcaEquipo(models.Model):
    tipoeq = models.ManyToManyField(TipoEquipo)
    marcaeq = models.CharField(max_length=150, unique=True, null=False, blank=False)
    
    def __str__(self):
        return f"{self.marcaeq}"
    
    class Meta:
        ordering = ['marcaeq']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
    
class ModeloEquipo(models.Model):
    tipoeq = models.ForeignKey(TipoEquipo, on_delete=models.PROTECT, null=False, blank=False)
    marcaeq = models.ForeignKey(MarcaEquipo, on_delete=models.PROTECT, null=False, blank=False)
    modeloeq = models.CharField(max_length=150, null=False,blank=False)

    def __str__(self):
        return f"{self.modeloeq} - {self.marcaeq}"
    
    class Meta:
        ordering = ['modeloeq']
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        constraints = [
            models.UniqueConstraint(fields=['tipoeq', 'marcaeq', 'modeloeq'], name='unique_tipoeq_marcaeq_modeloeq')
        ]

class EstadoEquipo(models.Model):
    estadoeq = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.estadoeq}"
    
    class Meta:
        ordering = ['estadoeq']
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

class TipoMttoEquipo(models.Model):
    tipomttoeq = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.tipomttoeq}"
    
    class Meta:
        ordering = ['tipomttoeq']
        verbose_name = 'Tipo de mantenimiento'
        verbose_name_plural = 'Tipos de mantenimiento'

class EstadoTareaOT(models.Model):
    estadotareaot = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.estadotareaot}"
    
    class Meta:
        ordering = ['estadotareaot']
        verbose_name = 'Estado de tarea'
        verbose_name_plural = 'Estados de tarea'

class EstadoOT(models.Model):
    estadoot = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.estadoot}"
    
    class Meta:
        ordering = ['estadoot']
        verbose_name = 'Estado de OT'
        verbose_name_plural = 'Estados de OT'
