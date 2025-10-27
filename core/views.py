
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from django.views.generic import ListView, TemplateView, CreateView
from .models import Provincia, Localidad

from django.urls import reverse_lazy
from .forms import ProvinciaForm
from django.http import JsonResponse



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    login_url = 'core:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bienvenido al Sistema de Gestión de Salud Mental'
        return context
    

class ProvinciaCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Provincia
    template_name = 'core/provincia_form.html'
    form_class = ProvinciaForm
    success_url = reverse_lazy('core:provincia_list')
    context_object_name = 'provincia'
    login_url = 'core:login'
    permission_required = 'core.add_provincia'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def form_valid(self, form):
        form.instance.provincia = form.cleaned_data['provincia']
        form.instance.pais = form.cleaned_data['pais']
        return super().form_valid(form)


class ProvinciaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Provincia
    template_name = 'provincia_list.html'
    context_object_name = 'provincias'
    login_url = 'core:login'
    permission_required = 'core.view_provincia'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_queryset(self):
        return Provincia.objects.all().order_by('provincia')

@login_required(login_url='core:login')
@permission_required('core.view_localidad', raise_exception=True)
def localidad_autocomplete(request):
    q = request.GET.get('q', '')
    localidades = Localidad.objects.filter(localidad__icontains=q)[:20]
    results = [{'id': loc.id, 'text': loc.localidad} for loc in localidades]
    return JsonResponse({'results': results})