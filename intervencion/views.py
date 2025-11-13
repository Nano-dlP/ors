from django.shortcuts import render


# Create your views here.

from django.views.generic import FormView
from .forms import IntervencionForm, IntervencionCreateForm
from .models import Intervencion
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView



#class IntevencionListView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
 #   template_name = 'intervencion/intervencion_listar.html'
  #  form_class = IntervencionForm
   # login_url = 'core:login'
#    permission_required = 'intervencion.view_intervencion'
 #   raise_exception = False
  #  success_url = reverse_lazy('intervencion:intervencion_list')

   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
     #   context['intervenciones'] = Intervencion.objects.all()
      #  return context





@login_required(login_url='core:login')
@permission_required('intervencion.view_intervencion', login_url='core:login', raise_exception=True)
def listar_intervenciones(request):
    intervenciones = Intervencion.objects.all()
    next_url = request.GET.get("next")       # para redirigir después

    return render(request, "intervencion/intervencion_list.html", {
        "intervenciones": intervenciones,
        "next_url": next_url,   # lo mandamos al template
    })

#class IntervencionCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
#    template_name = 'intervencion/intervencion_crear.html'
#    form_class = IntervencionCreateForm
#    success_url = reverse_lazy('intervencion:intervencion_list')
#    login_url = 'core:login'
#    permission_required = 'intervencion.add_intervencion'
#    raise_exception = False

#    def get_initial(self):
#        initial = super().get_initial()
#        expediente_id = self.request.GET.get('expediente_id')
#        if expediente_id:
#            initial['expediente'] = expediente_id
#        return initial

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        expediente_id = self.request.GET.get('expediente_id')
#        context['expediente_id'] = expediente_id  # Pasa el ID al template
#        if expediente_id:
#            from expediente.models import Expediente
#            try:
#                expediente = Expediente.objects.get(pk=expediente_id)
#                context['expediente_seleccionado'] = expediente  # Puedes mostrar datos del expediente
#            except Expediente.DoesNotExist:
#                context['expediente_seleccionado'] = None
#        return context

#    def form_valid(self, form):
#        form.save()
#        return super().form_valid(form)



class IntervencionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Intervencion
    form_class = IntervencionCreateForm
    template_name = 'intervencion/intervencion_crear.html'
    success_url = reverse_lazy('intervencion:intervencion_list')
    login_url = 'core:login'
    permission_required = 'intervencion.add_intervencion'
    raise_exception = False

    def get_initial(self):
        initial = super().get_initial()
        expediente_id = self.request.GET.get('expediente_id')
        if expediente_id:
            initial['expediente'] = expediente_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente_id = self.request.GET.get('expediente_id')
        context['expediente_id'] = expediente_id  # Pasa el ID al template
        if expediente_id:
            from expediente.models import Expediente
            try:
                expediente = Expediente.objects.get(pk=expediente_id)
                context['expediente_seleccionado'] = expediente  # Puedes mostrar datos del expediente
            except Expediente.DoesNotExist:
                context['expediente_seleccionado'] = None
        return context
    


class IntevencionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Intervencion
    template_name = 'intervencion/intervencion_listar.html'
    context_object_name = 'intervenciones'
    login_url = 'core:login'
    permission_required = 'intervencion.view_intervencion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso
    
    def get_queryset(self):
        return Intervencion.objects.all().order_by('-fecha_intervencion')
    


class IntervencionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Intervencion
    form_class = IntervencionCreateForm
    template_name = 'intervencion/intervencion_crear.html'
    success_url = reverse_lazy('intervencion:intervencion_list')
    context_object_name = 'intervenciones'
    login_url = 'core:login'
    permission_required = 'intervencion.change_intervencion'
    raise_exception = False  # devuelve 403 si no tiene permiso



class IntervencionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Intervencion
    template_name = 'intervencion/intervencion_detalle.html'
    context_object_name = 'intervencion'
    login_url = 'core:login'
    permission_required = 'intervencion.view_intervencion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso