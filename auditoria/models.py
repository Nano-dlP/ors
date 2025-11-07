from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings  # importa AUTH_USER_MODEL dinámicamente
from expediente.models import Expediente

class AuditoriaExpediente(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
    ]

    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='auditorias')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=10, choices=ACCIONES)
    observacion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - {self.expediente.identificador}"
