# tu_app/models.py
from django.contrib.auth.models import AbstractUser
#from django.core.exceptions import ValidationError
from django.db import models
from core.models import Localidad, Sede

class CustomUser(AbstractUser):
    dni = models.CharField(verbose_name ='DNI', max_length=15, blank=True, null=True)
    telefono = models.CharField(verbose_name = 'Teléfono', max_length=20, blank=True, null=True)
    direccion = models.CharField(verbose_name = 'Domicilio', blank=True, null=True)
    localidad = models.ForeignKey(Localidad, verbose_name = 'Localidad' ,on_delete=models.SET_NULL, null=True, blank=True)
    sede = models.ForeignKey(Sede, verbose_name = 'Sede', on_delete=models.SET_NULL, null=True, blank=True)
    foto_perfil = models.ImageField(verbose_name = 'Foto de Perfil', upload_to='perfiles/', blank=True, null=True)

    #def clean(self):
    #    super().clean()
    #    if CustomUser.objects.filter(dni=self.dni).exclude(pk=self.pk).exists():
    #        raise ValidationError({'dni': "Ya existe un usuario con este DNI."})

    def __str__(self):
        return f"{self.username} ({self.dni}) {self.localidad}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
