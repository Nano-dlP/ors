from django.urls import path
from auditoria.views import AuditoriaExpedienteListView, AuditoriaInstitucionListView, AuditoriaInternacionListView, AuditoriaIntervencionListView, AuditoriaPersonaListView, AuditoriaProfesionalListView, AuditoriaUsuarioListView

app_name = "auditoria"

urlpatterns = [
    path("expedientes/", AuditoriaExpedienteListView.as_view(), name="auditoria_expediente_list"),
    path("instituciones/", AuditoriaInstitucionListView.as_view(), name="auditoria_institucion_list"),
    path("internaciones/", AuditoriaInternacionListView.as_view(), name="auditoria_internacion_list"),
    path("intervenciones/", AuditoriaIntervencionListView.as_view(), name="auditoria_intervencion_list"),
    path("personas/", AuditoriaPersonaListView.as_view(), name="auditoria_persona_list"),
    path("profesionales/", AuditoriaProfesionalListView.as_view(), name="auditoria_profesional_list"),
    path("usuarios/", AuditoriaUsuarioListView.as_view(), name="auditoria_usuario_list"),
]
