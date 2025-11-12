from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Internacion
from .forms import InternacionForm
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
        context = super().get_context_data(**kwargs)
        expediente_institucion_id = self.kwargs.get('expediente_institucion_id')
        if expediente_institucion_id:
            context['expediente_institucion'] = get_object_or_404(
                ExpedienteInstitucion,
                id=expediente_institucion_id
            )

        # Indicar que es edición
        context['editar'] = True    
        return context


    def form_valid(self, form):
        """Asigna usuario y expediente_institucion antes de guardar."""
        form.instance.usuario = self.request.user

        expediente_institucion_id = self.kwargs.get('expediente_institucion_id')
        if expediente_institucion_id:
            form.instance.expediente_institucion = get_object_or_404(
                ExpedienteInstitucion,
                id=expediente_institucion_id
            )

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
    

class InternacionDetailView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Internacion
    template_name = 'internacion/internacion_detalle.html'
    context_object_name = 'internacion'
    login_url = 'core:login'
    permission_required = 'internacion.view_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['expediente_institucion'] = get_object_or_404(Internacion, pk=pk)
        context['expediente_institucion'] = Internacion
        return context
    

class InternacionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Internacion
    form_class = InternacionForm
    template_name = 'internacion/internacion_crear.html'
    success_url = reverse_lazy('internacion:internacion_list')
    context_object_name = 'internaciones'
    login_url = 'core:login'
    permission_required = 'internacion.change_internacion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso
    
    def form_valid(self, form):
        internacion = form.save(commit=False)
        # Si el formulario no envió expediente_institucion, mantener el existente
        if not form.cleaned_data.get('expediente_institucion'):
            internacion.expediente_institucion = self.get_object().expediente_institucion
        internacion.save()
        return super().form_valid(form)
