from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # importa AUTH_USER_MODEL dinámicamente
from expediente.models import Expediente, ExpedientePersona, ExpedienteInstitucion
from institucion.models import Institucion
from internacion.models import Internacion
from intervencion.models import Intervencion
from persona.models import Persona
from profesional.models import Profesional


class AuditoriaExpediente(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    expediente = models.ForeignKey(Expediente, on_delete=models.SET_NULL, related_name='auditorias_expediente', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - {self.expediente.identificador}"
    

class AuditoriaInstitucion(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]
    
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, related_name='auditorias_institucion', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - {self.institucion.nombre}"    


class AuditoriaInternacion(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    internacion = models.ForeignKey(Internacion, on_delete=models.SET_NULL, related_name='auditorias_internacion', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - Internación ID {self.internacion.id}"   
    

class AuditoriaIntervencion(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    intervencion = models.ForeignKey(Intervencion, on_delete=models.SET_NULL, related_name='auditorias_intervencion', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - Intervención ID {self.intervencion.id}"
    


class AuditoriaPersona(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, related_name='auditorias_persona', null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - {self.persona.nombre_completo()}"
    

class AuditoriaProfesional(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    profesional = models.ForeignKey(
        'profesional.Profesional',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='auditorias_profesional'
    )
    nombre_profesional = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        profesional_nombre = self.nombre_profesional or (self.profesional and self.profesional.user.get_full_name()) or "—"
        return f"{profesional_nombre} - {self.get_accion_display()} - {self.fecha_hora:%d/%m/%Y %H:%M}"

    @property
    def profesional_nombre(self):
        if self.profesional:
            return self.profesional.user.get_full_name()
        return "—"



class AuditoriaUsuario(models.Model):
    ACCIONES = [
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('CAMBIO_PASSWORD', 'Cambio de Contraseña'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='auditorias_usuario', null=True, blank=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()}"
    

class AuditoriaExpedientePersona(models.Model):

    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    # 🔹 ID histórico (si el registro se elimina)
    expediente_persona_id_original = models.IntegerField(null=True, blank=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=10, choices=ACCIONES)

    expediente_id = models.IntegerField(null=True, blank=True)
    expediente_numero = models.CharField(max_length=100, null=True, blank=True)

    persona_id = models.IntegerField(null=True, blank=True)
    persona_nombre = models.CharField(max_length=255, null=True, blank=True)

    rol_id = models.IntegerField(null=True, blank=True)
    rol_nombre = models.CharField(max_length=255, null=True, blank=True)

    observacion = models.TextField(blank=True, null=True)

    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - Exp:{self.expediente_id}"
    

class AuditoriaExpedienteInstitucion(models.Model):

    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    # 🔹 ID histórico del registro relación expediente-institución
    expediente_institucion_id_original = models.IntegerField(null=True, blank=True)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=10, choices=ACCIONES)

    # 🔹 Datos del expediente
    expediente_id = models.IntegerField(null=True, blank=True)
    expediente_numero = models.CharField(max_length=100, null=True, blank=True)

    # 🔹 Datos de la institución
    institucion_id = models.IntegerField(null=True, blank=True)
    institucion_nombre = models.CharField(max_length=255, null=True, blank=True)

    # 🔹 Datos de internación (opcional)
    internacion_id = models.IntegerField(null=True, blank=True)
    internacion_descripcion = models.CharField(max_length=255, null=True, blank=True)

    observacion = models.TextField(blank=True, null=True)

    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - Exp:{self.expediente_id}"