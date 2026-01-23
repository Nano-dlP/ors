from django.db import models
from django.utils import timezone
from core.models import Sede, Rol
from persona.models import Persona
from institucion.models import Institucion
from expediente.managers import ExpedienteManager



# Create your models here.
class TipoSolicitud(models.Model):
    tipo_solicitud = models.CharField(max_length=50, verbose_name="Tipo de Solicitud")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_solicitud
    
    class Meta:
        verbose_name = 'Tipo de solicitud'
        verbose_name_plural = 'Tipos de solicitudes'



class GrupoEtario(models.Model):
    grupo_etario = models.CharField(max_length=50, verbose_name="Grupo Etario")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.grupo_etario
    
    class Meta:
        verbose_name = 'Grupo Etario'
        verbose_name_plural = 'Grupos etarios'


    
class ResumenIntervencion(models.Model):
    resumen_intervencion = models.CharField(max_length=50, verbose_name="Resumen de Intervención")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.resumen_intervencion    
    
    class Meta:
        verbose_name = 'Resumen de Intervención'
        verbose_name_plural = 'Resumenes de intervenciones'


    
class TipoPatrocinio(models.Model):
    tipo_patrocinio = models.CharField(max_length=50, verbose_name="Tipo de Patrocinio")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_patrocinio

    class Meta:
        verbose_name = 'Tipo de patrocinio'
        verbose_name_plural = 'Tipos de patrocinios'



class MedioIngreso(models.Model):
    medio_ingreso = models.CharField(max_length=50, verbose_name="Medio de Ingreso")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.medio_ingreso
    
    class Meta:
        verbose_name = 'Medio de Ingreso'
        verbose_name_plural = 'Medios de Ingresos'



class EstadoExpediente(models.Model):
    estado_expediente = models.CharField(max_length=100, verbose_name="Estado el expediente")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.estado_expediente
    
    class Meta:
        verbose_name = 'Estado del expediente'
        verbose_name_plural = 'Estado de los expedientes'



class Expediente(models.Model):
    numero = models.PositiveIntegerField("Número de expediente")
    anio = models.PositiveIntegerField("Año del expediente", default=2025)
    abreviatura = models.CharField("Abreviatura", max_length=4)
    fecha_creacion = models.DateField("Fecha de creación", auto_now_add=False)
    identificador = models.CharField("Identificador del expediente", max_length=100, unique=True, editable=False)
    
    fecha_de_juzgado = models.DateField(blank=True, null=True, verbose_name='Fecha del Juzgado')
    fecha_de_recepcion = models.DateField(blank=True, null=True, verbose_name='Fecha de Recepción')
    cuij = models.CharField(blank=True, max_length=50, null=True, verbose_name='CUIJ')
    clave_sisfe = models.CharField(blank=True, max_length=50, null=True, verbose_name='Clave SISFE')
    
    estado_expediente = models.ForeignKey(EstadoExpediente, on_delete=models.CASCADE, related_name='expediente_estado_expediente')
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, verbose_name='Sede')
    medio_ingreso = models.ForeignKey(MedioIngreso, on_delete=models.CASCADE, blank=True, null=True)
    expediente_fisico = models.BooleanField(default=False)
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE)
    
    tipo_patrocinio = models.ForeignKey(TipoPatrocinio, on_delete=models.CASCADE, null=True, blank=True)
    resumen_intervencion = models.ForeignKey(ResumenIntervencion, on_delete=models.CASCADE, blank=True, null=True)

    edad_persona = models.PositiveIntegerField(blank=True, null=True)
    grupo_etario = models.ForeignKey(GrupoEtario, related_name='expediente_grupo_etario', on_delete=models.CASCADE)
    situacion_habitacional_hist = models.CharField(verbose_name= 'Situación habitacional historica', max_length=255, blank=True, null=True)
    observaciones = models.TextField(verbose_name='Observaviones', blank=True, null=True)

    estado = models.BooleanField("Estado", default=True)

    objects = ExpedienteManager()

    class Meta:
        unique_together = ('numero', 'anio', 'abreviatura')
        ordering = ['-anio', '-numero']

    def save(self, *args, **kwargs):
        if not self.pk:
            today = timezone.now().date()
            self.anio = today.year
            # Tomar la abreviatura desde la sede si no está cargada
            if not self.abreviatura and self.sede:
                self.abreviatura = self.sede.abreviatura.upper()
            # Obtener el último número para esa sede y año
            ultimo = Expediente.objects.filter(
                sede=self.sede,
                anio=self.anio
            ).order_by('-numero').first()
            self.numero = (ultimo.numero + 1) if ultimo else 1
            # Crear identificador
            self.identificador = f"{self.abreviatura}-{str(self.numero).zfill(5)}-{self.anio}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.identificador



class ExpedienteDocumento(models.Model):
    expediente = models.ForeignKey(
        'Expediente',
        related_name='documentos',
        on_delete=models.CASCADE
    )
    nombre = models.CharField("Nombre del documento", max_length=255, blank=True, null=True)
    archivo = models.FileField("Archivo", upload_to="documentos/expedientes/")
    fecha_subida = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre or 'Documento'}"



class ExpedientePersona(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='expedientepersona_expediente')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='expedientepersona_persona')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='expedientepersona_rol')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['expediente', 'persona', 'rol'],
                                    name='unique_expediente_persona_rol'),
        ]

    def __str__(self):
        return f"{self.expediente} - {self.persona}"



class ExpedienteInstitucion(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='expedienteinstitucion_expediente')
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='expedienteinstitucion_institucion')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='expedienteinstitucion_rol')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['expediente', 'institucion', 'rol'],
                                    name='unique_expediente_institucion_rol'),
        ]
        
    def __str__(self):
        return str(self.expediente)
    

    
