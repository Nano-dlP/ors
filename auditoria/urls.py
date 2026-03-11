from django.urls import path
from auditoria.views import (
                                AuditoriaExpedienteListView, 
                                AuditoriaExpedienteInstitucionListView, 
                                AuditoriaExpedientePersonaListView, 
                                AuditoriaInstitucionListView, 
                                AuditoriaInternacionListView, 
                                AuditoriaIntervencionListView, 
                                AuditoriaPersonaListView, 
                                AuditoriaProfesionalListView, 
                                AuditoriaUsuarioListView)

app_name = "auditoria"

urlpatterns = [
    path("auditoria/expedientes/", AuditoriaExpedienteListView.as_view(), name="auditoria_expediente_list"),
    path("auditoria/expediente_personas/", AuditoriaExpedientePersonaListView.as_view(), name="auditoria_expediente_persona_list"),
    path("auditoria/expediente_instituciones/", AuditoriaExpedienteInstitucionListView.as_view(), name="auditoria_expediente_institucion_list"),
    path("auditoria/instituciones/", AuditoriaInstitucionListView.as_view(), name="auditoria_institucion_list"),
    path("auditoria/internaciones/", AuditoriaInternacionListView.as_view(), name="auditoria_internacion_list"),
    path("auditoria/intervenciones/", AuditoriaIntervencionListView.as_view(), name="auditoria_intervencion_list"),
    path("auditoria/personas/", AuditoriaPersonaListView.as_view(), name="auditoria_persona_list"),
    path("auditoria/profesionales/", AuditoriaProfesionalListView.as_view(), name="auditoria_profesional_list"),
    path("auditoria/usuarios/", AuditoriaUsuarioListView.as_view(), name="auditoria_usuario_list"),
]
