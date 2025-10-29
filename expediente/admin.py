from django.contrib import admin
from .models import TipoSolicitud, GrupoEtario,  ResumenIntervencion, TipoPatrocinio, MedioIngreso, EstadoExpediente

#admin.site.register(TipoSolicitud)
admin.site.register(GrupoEtario)
admin.site.register(ResumenIntervencion)
admin.site.register(TipoPatrocinio)
admin.site.register(MedioIngreso)
admin.site.register(EstadoExpediente)
admin.site.register(TipoSolicitud)

# Register your models here.

