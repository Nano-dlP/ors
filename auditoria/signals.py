from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .utils import get_client_ip
from expediente.models import Expediente, ExpedientePersona, ExpedienteInstitucion
from institucion.models import Institucion
from internacion.models import Internacion
from intervencion.models import Intervencion
from persona.models import Persona
from profesional.models import Profesional



from auditoria.models import (
                                AuditoriaExpediente, 
                                AuditoriaInstitucion, 
                                AuditoriaInternacion, 
                                AuditoriaIntervencion, 
                                AuditoriaPersona, 
                                AuditoriaProfesional, 
                                AuditoriaUsuario, 
                                AuditoriaExpedientePersona, 
                                AuditoriaExpedienteInstitucion
                            )
from threading import local

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_user  # Asegurate de tener django-crum instalado
from .models import Profesional, AuditoriaProfesional


_user = local()



# Middleware-friendly setter (para capturar el usuario actual)
def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, "value", None)


#########################USUARIO####################################

@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    AuditoriaUsuario.objects.create(
        usuario=user,
        accion='LOGIN',
        observacion='Usuario inició sesión',
        ip=get_client_ip(request),
    )

@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    AuditoriaUsuario.objects.create(
        usuario=user,
        accion='LOGOUT',
        observacion='Usuario cerró sesión',
        ip=get_client_ip(request),
    )

@receiver(user_login_failed)
def registrar_login_fallido(sender, credentials, request, **kwargs):
    username = credentials.get('username', 'desconocido')
    ip = get_client_ip(request) if request else None

    AuditoriaUsuario.objects.create(
        usuario=None,
        accion='LOGIN_FAILED',
        observacion=f"Intento de login fallido para el usuario: {username}",
        ip=ip,
    )


#########################EXPEDIENTE####################################
@receiver(post_save, sender=Expediente)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaExpediente.objects.create(
        expediente=instance,
        usuario=usuario,
        accion=accion,
        observacion=f"Expediente {'creado' if created else 'editado'}."
    )


@receiver(post_delete, sender=Expediente)
def registrar_auditoria_eliminado(sender, instance, **kwargs):
    usuario = get_current_user()
    AuditoriaExpediente.objects.create(
        expediente=instance,
        usuario=usuario,
        accion='ELIMINAR',
        observacion="Expediente eliminado del sistema."
    )


#########################INSTITUCION#####################################
@receiver(post_save, sender=Institucion)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaInstitucion.objects.create(
        institucion=instance,
        usuario=usuario,
        accion=accion,
        observacion=f"Institución {'creada' if created else 'editada'}."
    )


@receiver(post_delete, sender=Institucion)
def registrar_auditoria_eliminado(sender, instance, **kwargs):
    usuario = get_current_user()
    AuditoriaInstitucion.objects.create(
        institucion=instance,
        usuario=usuario,
        accion='ELIMINAR',
        observacion="Institución eliminada del sistema."
    )


##############################INTERNACION#############################################
@receiver(post_save, sender=Internacion)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaInternacion.objects.create(
        internacion=instance,
        usuario=usuario,
        accion=accion,
        observacion=f"Internación {'creada' if created else 'editada'}."
    )


@receiver(pre_delete, sender=Internacion)
def registrar_auditoria_eliminado(sender, instance, **kwargs):
    usuario = get_current_user()
    AuditoriaInternacion.objects.create(
        internacion=instance,
        usuario=usuario,
        accion='ELIMINAR',
        observacion="Internación eliminada del sistema."
    )


#############################INTERVENCION##############################################
@receiver(post_save, sender=Intervencion)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaIntervencion.objects.create(
        intervencion=instance,
        usuario=usuario,
        accion=accion,
        observacion=f"Intervención {'creada' if created else 'editada'}."
    )


@receiver(post_delete, sender=Intervencion)
def registrar_auditoria_eliminado(sender, instance, **kwargs):
    usuario = get_current_user()
    AuditoriaIntervencion.objects.create(
        intervencion=instance,
        usuario=usuario,
        accion='ELIMINAR',
        observacion="Intervención eliminada del sistema."
    )


############################PERSONA#########################################
@receiver(post_save, sender=Persona)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaPersona.objects.create(
        persona=instance,
        usuario=usuario,
        accion=accion,
        observacion=f"Persona {'creada' if created else 'editada'}."
    )


@receiver(post_delete, sender=Persona)
def registrar_auditoria_eliminado(sender, instance, **kwargs):
    usuario = get_current_user()
    AuditoriaPersona.objects.create(
        persona=instance,
        usuario=usuario,
        accion='ELIMINAR',
        observacion="Persona eliminada del sistema."
    )


#############################PROFESIONAL##############################################

@receiver(post_save, sender=Profesional)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaProfesional.objects.create(
        profesional=instance,
        nombre_profesional=instance.user.get_full_name(),
        usuario=usuario,
        accion=accion,
        observacion=f"Profesional {'creado' if created else 'editado'}."
    )


@receiver(post_delete, sender=Profesional)
def registrar_auditoria_eliminado(sender, instance, **kwargs):
    usuario = get_current_user()
    AuditoriaProfesional.objects.create(
        profesional=None,
        nombre_profesional=instance.user.get_full_name(),
        usuario=usuario,
        accion='ELIMINAR',
        observacion="Profesional eliminado del sistema."
    )

#############################USUARIO##############################################



@receiver(pre_delete, sender=ExpedientePersona)
def auditoria_eliminar(sender, instance, **kwargs):
    usuario = get_current_user()

    AuditoriaExpedientePersona.objects.create(
        expediente_persona_id_original=instance.id,
        usuario=usuario,
        accion='ELIMINAR',

        expediente_id=instance.expediente.id if instance.expediente else None,
        expediente_numero=str(instance.expediente) if instance.expediente else None,

        persona_id=instance.persona.id if instance.persona else None,
        persona_nombre=str(instance.persona) if instance.persona else None,

        rol_id=instance.rol.id if instance.rol else None,
        rol_nombre=str(instance.rol) if instance.rol else None,

        observacion="Relación entre expediente y persona eliminada del sistema."
    )


@receiver(pre_delete, sender=ExpedienteInstitucion)
def auditoria_eliminar(sender, instance, **kwargs):

    usuario = get_current_user()

    internacion = instance.internacion_expedienteinstitucion.first()

    AuditoriaExpedienteInstitucion.objects.create(
        expediente_institucion_id_original=instance.id,
        usuario=usuario,
        accion='ELIMINAR',

        expediente_id=instance.expediente.id,
        expediente_numero=str(instance.expediente),

        institucion_id=instance.institucion.id,
        institucion_nombre=str(instance.institucion),

        internacion_id=internacion.id if internacion else None,
        internacion_descripcion=str(internacion) if internacion else None,

        observacion="Relación expediente - institución eliminada."
    )