from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from expediente.models import Expediente
from auditoria.models import AuditoriaExpediente
from threading import local

_user = local()

# Middleware-friendly setter (para capturar el usuario actual)
def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, "value", None)


@receiver(post_save, sender=Expediente)
def registrar_auditoria_guardado(sender, instance, created, **kwargs):
    usuario = get_current_user()
    accion = 'CREAR' if created else 'EDITAR'
    AuditoriaExpediente.objects.create(
        expediente=instance,
        usuario=usuario,
        accion=accion,
        observacion=f"Expediente {'creado' if created else 'editado'} automáticamente."
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
