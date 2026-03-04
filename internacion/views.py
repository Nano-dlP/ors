from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Internacion
from .forms import InternacionForm, InternacionMotivoInternacionForm
from expediente.models import ExpedienteInstitucion
# Create your views here.

class InternacionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Internacion
    form_class = InternacionForm
    template_name = 'internacion/internacion_crear.html'
    success_url = reverse_lazy('internacion:internacion_list')  # Ajustá si querés volver al expediente
    context_object_name = 'internaciones'
    login_url = 'core:login'
    permission_required = 'internacion.add_internacion'
    raise_exception = False  # devuelve 403 si no tiene permiso

    def get_initial(self):
        """Pre-carga el expediente_institucion si se recibe por la URL."""
        initial = super().get_initial()
        expediente_institucion_id = self.kwargs.get('expediente_institucion_id')
        if expediente_institucion_id:
            initial['expediente_institucion'] = expediente_institucion_id
        return initial
    

    def get_context_data(self, **kwargs):
        """Agrega el expediente_institucion al contexto para mostrarlo en el template."""
        context = super().get_context_data(**kwargs)
        expediente_institucion_id = self.kwargs.get('expediente_institucion_id')
        expediente_institucion = get_object_or_404(ExpedienteInstitucion, id=expediente_institucion_id)
        context['expediente_institucion'] = expediente_institucion
        return context

    def form_valid(self, form):
        """Asigna usuario y expediente_institucion antes de guardar."""
        form.instance.usuario = self.request.user
        expediente_institucion_id = self.kwargs.get('expediente_institucion_id')
        form.instance.expediente_institucion = get_object_or_404(ExpedienteInstitucion, id=expediente_institucion_id)
        return super().form_valid(form)


class InternacionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Internacion
    template_name = 'internacion/internacion_list.html'
    context_object_name = 'internaciones'
    login_url = 'core:login'
    permission_required = 'internacion.view_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso
    
    def get_queryset(self):
        return Internacion.objects.all().order_by('-fecha_internacion')
    

class InternacionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Internacion
    template_name = 'internacion/internacion_detalle.html'
    context_object_name = 'internacion'
    login_url = 'core:login'
    permission_required = 'internacion.view_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso
  
   
class InternacionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Internacion
    form_class = InternacionForm
    template_name = 'internacion/internacion_crear.html'
    success_url = reverse_lazy('internacion:internacion_list')
    context_object_name = 'internaciones'
    login_url = 'core:login'
    permission_required = 'internacion.change_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        internacion = self.get_object()  # obtiene la instancia que se está editando

        # Pasamos la información de expediente_institucion al template
        context['expediente_institucion'] = internacion.expediente_institucion

        # Indicador de que estamos en modo edición
        context['editar'] = True
        return context
    
    def form_valid(self, form):
        internacion = form.save(commit=False)
        # Si el formulario no envió expediente_institucion, mantener el existente
        if not form.cleaned_data.get('expediente_institucion'):
            internacion.expediente_institucion = self.get_object().expediente_institucion
        internacion.save()
        return super().form_valid(form)


class InternacionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Internacion
    template_name = 'internacion/internacion_confirm_delete.html'
    success_url = reverse_lazy('internacion:internacion_list')
    context_object_name = 'internacion'
    login_url = 'core:login'
    permission_required = 'internacion.delete_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso


class InternacionMotivoInternacion(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'internacion/internacion_motivo_internacion.html'
    login_url = 'core:login'
    permission_required = 'internacion.view_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = InternacionMotivoInternacionForm(self.request.GET or None)

        total = 0
        detalle = []

        if form.is_valid():
            resultado = Internacion.objects.internacion_motivo_internacion(
                fecha_desde=form.cleaned_data.get("fecha_desde"),
                fecha_hasta=form.cleaned_data.get("fecha_hasta"),
                tipo_internacion_id=form.cleaned_data.get("tipo_internacion").id
                    if form.cleaned_data.get("tipo_internacion") else None,
                grupo_etario_id=form.cleaned_data.get("grupo_etario").id
                    if form.cleaned_data.get("grupo_etario") else None,
                sede_id=form.cleaned_data.get("sede").id
                    if form.cleaned_data.get("sede") else None,
            )

            total = resultado["total_general"]
            detalle = resultado["detalle"]

        context["form"] = form
        context["total"] = total
        context["detalle"] = detalle

        return context


class InternacionMotivoAlta(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'internacion/internacion_motivo_alta.html'
    login_url = 'core:login'
    permission_required = 'internacion.view_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """Reutilizamos el mismo formulario de filtros que en motivo internación."""
        form = InternacionMotivoInternacionForm(self.request.GET or None)

        total = 0
        detalle = []

        if form.is_valid():
            resultado = Internacion.objects.internacion_motivo_alta(
                fecha_desde=form.cleaned_data.get("fecha_desde"),
                fecha_hasta=form.cleaned_data.get("fecha_hasta"),
                tipo_internacion_id=form.cleaned_data.get("tipo_internacion").id
                    if form.cleaned_data.get("tipo_internacion") else None,
                grupo_etario_id=form.cleaned_data.get("grupo_etario").id
                    if form.cleaned_data.get("grupo_etario") else None,
                sede_id=form.cleaned_data.get("sede").id
                    if form.cleaned_data.get("sede") else None,
            )

            total = resultado["total_general"]
            detalle = resultado["detalle"]

        context["form"] = form
        context["total"] = total
        context["detalle"] = detalle

        return context
    

def dashboard_motivo_alta(request):

    data = Internacion.objects.internacion_motivo_alta(
        fecha_desde=request.GET.get("fecha_desde"),
        fecha_hasta=request.GET.get("fecha_hasta"),
        tipo_internacion_id=request.GET.get("tipo_internacion"),
        grupo_etario_id=request.GET.get("grupo_etario"),
        sede_id=request.GET.get("sede"),
    )

    context = {
        "total_general": data["total_general"],
        "detalle": list(data["detalle"]),
    }

    return render(
        request,
        "internacion/dashboard_motivo_alta.html",
        context
    )
