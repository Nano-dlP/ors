from django.contrib import admin

from .models import Pais, Provincia, Genero, Nivel_Educativo, Tipo_Documento, Sede, Localidad, Rol, AreaProfesional, Profesion, SituacionHabitacional
from .models import ClienteLog
# Register your models here.

admin.site.register(Provincia)
admin.site.register(Pais)
admin.site.register(Genero)
admin.site.register(Nivel_Educativo)
admin.site.register(Tipo_Documento)
admin.site.register(Sede)
#admin.site.register(Localidad)
admin.site.register(Rol)
admin.site.register(AreaProfesional)
admin.site.register(Profesion)
admin.site.register(SituacionHabitacional)

admin.site.site_header = 'Salud Mental Admin'
admin.site.site_title = 'Salud Mental Admin Portal'
admin.site.index_title = 'Bienvenido al portal de administración de Salud Mental'
admin.site.empty_value_display = 'N/A'

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    ordering = ('localidad',)


@admin.register(ClienteLog)
class ClienteLogAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'ip', 'navegador', 'sistema_operativo', 'url')
    search_fields = ('ip', 'usuario__username', 'user_agent', 'url', 'referer')
    list_filter = ('fecha', 'sistema_operativo', 'navegador')
    readonly_fields = [f.name for f in ClienteLog._meta.fields]
    ordering = ['-fecha']

    def has_add_permission(self, request):
        return False  # solo lectura

    def has_change_permission(self, request, obj=None):
        return False  # evitar edición

    def has_delete_permission(self, request, obj=None):
        return False  # evitar eliminación