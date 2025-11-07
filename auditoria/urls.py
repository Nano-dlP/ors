from django.urls import path
from auditoria.views import AuditoriaExpedienteListView

app_name = "auditoria"

urlpatterns = [
    path("expedientes/", AuditoriaExpedienteListView.as_view(), name="auditoria_expediente_list"),
]
