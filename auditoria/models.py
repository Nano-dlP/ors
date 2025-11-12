from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # importa AUTH_USER_MODEL dinámicamente
from expediente.models import Expediente
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

    expediente = models.ForeignKey(Expediente, on_delete=models.SET_NULL, related_name='auditorias', null=True, blank=True)
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
    
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, related_name='auditorias', null=True, blank=True)
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

    internacion = models.ForeignKey(Internacion, on_delete=models.SET_NULL, related_name='auditorias', null=True, blank=True)
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

    intervencion = models.ForeignKey(Intervencion, on_delete=models.SET_NULL, related_name='auditorias', null=True, blank=True)
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

    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, related_name='auditorias', null=True, blank=True)
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
        related_name='auditorias'
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
    


