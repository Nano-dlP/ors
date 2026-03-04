from django.utils import timezone

from django.db import models

from expediente.models import ExpedienteInstitucion

from .managers import InternacionManager

# Create your models here.
class MotivoInternacion(models.Model):
    motivo_internacion = models.CharField(max_length=50, verbose_name="Motivo de Internación")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.motivo_internacion
    
    class Meta:
        verbose_name = "Motivo de Internación"
        verbose_name_plural = "Motivos de Internación"
        ordering = ['-id']


class MotivoAlta(models.Model):
    motivo_alta = models.CharField(max_length=50, verbose_name="Motivo de Alta")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.motivo_alta
    
    class Meta:
        verbose_name = "Motivo de Alta"
        verbose_name_plural = "Motivos de Alta"
        ordering = ['-id']


class ModalidadSuicidio(models.Model):
    modalidad_suicidio = models.CharField(max_length=50, verbose_name="Modalidad de Suicidio")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.modalidad_suicidio

    class Meta:
        verbose_name = "Modalidad de Suicidio"
        verbose_name_plural = "Modalidades de Suicidio"
        ordering = ['-id']


class TipoAdiccion(models.Model):
    tipo_adiccion = models.CharField(max_length=50, verbose_name="Tipo de Adicción")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.tipo_adiccion
    
    class Meta:
        verbose_name = "Tipo de Adicción"
        verbose_name_plural = "Tipos de Adicción"
        ordering = ['-id']


class TipoInternacion(models.Model):
    tipo_internacion = models.CharField(max_length=50, verbose_name="Tipo de Internación")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_internacion

    class Meta:
        verbose_name = "Tipo de Internación"
        verbose_name_plural = "Tipos de Internación"
        ordering = ['-id']


class Internacion(models.Model):
    expediente_institucion = models.ForeignKey(ExpedienteInstitucion, on_delete=models.CASCADE, related_name='internacion_expedienteinstitucion', blank=True, null=True)
    fecha_internacion = models.DateField('Fecha de internación', auto_now=False, auto_now_add=False, blank=True, null=True) 
    fecha_alta = models.DateField('Fecha de alta o derivación', auto_now=False, auto_now_add=False, blank=True, null=True) 
    motivo_internacion = models.ForeignKey(MotivoInternacion, on_delete=models.CASCADE, related_name='internacion_motivo_internacion', blank=True, null=True)
    motivo_alta = models.ForeignKey(MotivoAlta, on_delete=models.CASCADE, related_name='internacion_motivo_alta', blank=True, null=True)
    tipo_internacion = models.ForeignKey(TipoInternacion, on_delete=models.CASCADE, related_name='internacion_tipo_internacion', blank=True, null=True)
    requisitos = models.CharField('Requisitos', max_length=50, blank=True, null=True)
    intento_suicidio = models.BooleanField('Intento de suicidio?', default=False)
    modalidad_suicidio = models.ForeignKey(ModalidadSuicidio, on_delete=models.CASCADE, related_name='internacion_modalidad_suicidio', blank=True, null=True)
    posee_adiccion = models.BooleanField('Posee adicciones?', default=False)
    tipo_adiccion = models.ForeignKey(TipoAdiccion, on_delete=models.CASCADE, related_name='internacion_tipo_adiccion', blank=True, null=True)
    fecha_cumplimiento = models.DateField('Fecha de cumplimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    observaciones = models.TextField('Observaciones', blank=True, null=True)
    estado = models.BooleanField('Estado', default=True)

    objects = InternacionManager()


    def save(self, *args, **kwargs):
        """
        Si la internación tiene una fecha de alta, se marca como inactiva (estado=False).
        """
        if self.fecha_alta:
            self.estado = False
        else:
            self.estado = True
        super(Internacion, self).save(*args, **kwargs)

    @property
    def dias_internado(self):
        if not self.fecha_internacion:
            return None

        fin = self.fecha_alta or timezone.localdate()
        return max((fin - self.fecha_internacion).days, 0)


    @property
    def dias_restantes(self):
        if not self.fecha_cumplimiento:
            return None

        dias = (self.fecha_cumplimiento - timezone.localdate()).days
        return max(dias, 0)


    @property
    def nivel_internacion(self):
        dias = self.dias_restantes
        if dias is None:
            return None
        if dias <= 30:
            return 'danger'
        if dias <= 60:
            return 'warning'
        return 'success'
    
    @property
    def alerta_dias_restantes(self):
        dias = self.dias_restantes

        if dias is None:
            return None

        if dias == 0:
            return {
                'tipo': 'danger',
                'mensaje': '⚠️ Plazo vencido'
            }

        if dias <= 30:
            if dias == 1:
                mensaje = '⚠️ Queda solo 1 día'
            else:
                mensaje = f'⚠️ Quedan solo {dias} días'
            return {
                'tipo': 'danger',
                'mensaje': mensaje
            }

        if dias <= 60:
            return {
                'tipo': 'warning',
                'mensaje': f'⏳ Quedan {dias} días'
            }

        return {
            'tipo': 'success',
            'mensaje': f'✔️ {dias} días restantes'
        }