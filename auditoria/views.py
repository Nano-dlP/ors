from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from auditoria.models import (
                                AuditoriaExpediente,
                                AuditoriaExpedienteInstitucion,
                                AuditoriaExpedientePersona, 
                                AuditoriaInstitucion, 
                                AuditoriaInternacion, 
                                AuditoriaIntervencion, 
                                AuditoriaPersona, 
                                AuditoriaProfesional, 
                                AuditoriaUsuario)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AuditoriaExpedienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaExpediente
    template_name = "auditoria/auditoria_expediente_list.html"
    context_object_name = "auditorias"
    permission_required = "expediente.view_expediente"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaExpediente.objects.select_related("usuario", "expediente").order_by("-fecha_hora")
    

class AuditoriaExpedientePersonaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaExpedientePersona
    template_name = "auditoria/auditoria_expediente_persona_list.html"
    context_object_name = "auditorias"
    permission_required = "expediente.view_expediente"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaExpedientePersona.objects.select_related("usuario").order_by("-fecha_hora")
    

class AuditoriaExpedienteInstitucionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaExpedienteInstitucion
    template_name = "auditoria/auditoria_expediente_institucion_list.html"
    context_object_name = "auditorias"
    permission_required = "expediente.view_expediente"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaExpedienteInstitucion.objects.select_related("usuario").order_by("-fecha_hora")


class AuditoriaInstitucionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaInstitucion
    template_name = "auditoria/auditoria_institucion_list.html"
    context_object_name = "auditorias"
    permission_required = "institucion.view_institucion"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaInstitucion.objects.select_related("usuario", "institucion").order_by("-fecha_hora")
    

class AuditoriaInternacionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaInternacion
    template_name = "auditoria/auditoria_internacion_list.html"
    context_object_name = "auditorias"
    permission_required = "internacion.view_internacion"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaInternacion.objects.select_related("usuario", "internacion").order_by("-fecha_hora")


class AuditoriaIntervencionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaIntervencion
    template_name = "auditoria/auditoria_intervencion_list.html"
    context_object_name = "auditorias"
    permission_required = "intervencion.view_intervencion"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaIntervencion.objects.select_related("usuario", "intervencion").order_by("-fecha_hora")        


class AuditoriaPersonaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaPersona
    template_name = "auditoria/auditoria_persona_list.html"
    context_object_name = "auditorias"
    permission_required = "persona.view_persona"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaPersona.objects.select_related("usuario", "persona").order_by("-fecha_hora")


class AuditoriaProfesionalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaProfesional
    template_name = "auditoria/auditoria_profesional_list.html"
    context_object_name = "auditorias"
    permission_required = "profesional.view_profesional"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaProfesional.objects.select_related("usuario", "profesional").order_by("-fecha_hora")


class AuditoriaUsuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaUsuario
    template_name = "auditoria/auditoria_usuario_list.html"
    context_object_name = "auditorias"
    permission_required = "auth.view_user"
    raise_exception = False
    #paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaUsuario.objects.select_related("usuario").order_by("-fecha_hora")

