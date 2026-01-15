from django.db import models

from core.models import Tipo_Documento, Genero,Nivel_Educativo, Localidad

#Conecto el modelo con la clase que se encuentra en el managers
from .managers import PersonaManagers


# Create your models here.
class Persona(models.Model):
    tipo_documento = models.ForeignKey(Tipo_Documento, verbose_name=("Documento tipo"), on_delete=models.CASCADE, related_name='persona_tipo_documento')
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name=("Número de documento"))
    nombre = models.CharField(max_length=50, verbose_name=("Nombre"))
    apellido = models.CharField(max_length=50, verbose_name=("Apellido"))
    fecha_nacimiento = models.DateField(verbose_name=("Fecha de nacimiento"), blank=True, null=True)
    genero = models.ForeignKey(Genero, verbose_name=("Género"), on_delete=models.CASCADE, related_name='persona_genero', blank=True, null=True)
    ciudad_nacimiento = models.CharField(max_length=100, verbose_name=("Ciudad de nacimiento"), blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name=("Teléfono"), blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name=("Correo electrónico"), blank=True, null=True)
    direccion_calle = models.CharField(max_length=50, verbose_name=("Calle"), blank=True, null=True)
    direccion_numero = models.CharField(max_length=10, verbose_name=("Número"), blank=True, null=True)
    direccion_piso = models.CharField(max_length=10, verbose_name=("Piso"), blank=True, null=True)
    direccion_depto = models.CharField(max_length=10, verbose_name=("Dto."), blank=True, null=True)
    localidad = models.ForeignKey(Localidad, verbose_name=("Localidad"), on_delete=models.CASCADE, related_name='persona_localidad', blank=True, null=True, help_text='Localidad donde habita actualmete')
    ciudad_nacimiento = models.CharField(max_length=100, verbose_name=("Ciudad de nacimiento"), blank=True, null=True)
    nivel_educativo = models.ForeignKey(Nivel_Educativo, verbose_name=("Nivel educativo"), on_delete=models.CASCADE, related_name='persona_nivel_educativo', blank=True, null=True)
    ocupacion = models.CharField(max_length=100, verbose_name=("Ocupación"), blank=True, null=True)
    posee_cobertura_salud = models.BooleanField(default=False, verbose_name=("Posee cobertura?"))
    cobertura_salud = models.CharField(max_length=100, verbose_name=("Cobertura de salud"), blank=True, null=True)
    posee_grupo_apoyo = models.BooleanField(default=False, verbose_name=("Posee grupo?"))
    grupo_apoyo = models.CharField(max_length=100, verbose_name=("Grupo de apoyo"), blank=True, null=True)
    derecho_seguridad_social = models.CharField(max_length=100, verbose_name=("Derecho a la seguridad social"), blank=True, null=True)
    administra_recursos = models.BooleanField(default=False, verbose_name=("Administra recursos?"))
    carnet_discapacidad = models.CharField(max_length=50, verbose_name=("Carnet de discapacidad"), blank=True, null=True)
    situacion_habitacional = models.CharField(max_length=100, verbose_name=("Situación habitacional"), blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True, verbose_name=("Estado"))
    carnet_unico_discapacidad = models.BooleanField(default=False, verbose_name=("Carnet único de discapacidad"))

    #Establezco la conexión a la clase
    objects = PersonaManagers()

    class Meta:
        permissions = [
            ("puede_crear_persona", "Puede crear una persona"),
        ]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"


    