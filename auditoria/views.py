from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from auditoria.models import AuditoriaExpediente
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AuditoriaExpedienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditoriaExpediente
    template_name = "auditoria/auditoria_expediente_list.html"
    context_object_name = "auditorias"
    permission_required = "expediente.view_expediente"
    raise_exception = False
    paginate_by = 25  # opcional, para paginación

    def get_queryset(self):
        return AuditoriaExpediente.objects.select_related("usuario", "expediente").order_by("-fecha_hora")
