from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .models import Institucion
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.urls import reverse
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from .forms import InstitucionForm



class InstitucionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Institucion
    template_name = 'institucion/institucion_form.html'
    form_class = InstitucionForm
    success_url = reverse_lazy('institucion:institucion_list')
    context_object_name = 'institucion'
    login_url = 'core:login'
    permission_required = 'institucion.add_institucion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)

        next_url = self.request.GET.get('next')
        if next_url:
            query_string = urlencode({'institucion_id': self.object.pk})
            return HttpResponseRedirect(f'{next_url}?{query_string}')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')  # 🔹 pasa el parámetro al template
        return context


class InstitucionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Institucion
    template_name = 'institucion/institucion_list.html'
    context_object_name = 'instituciones'
    login_url = 'core:login'
    permission_required = 'institucion.view_institucion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_queryset(self):
        return Institucion.objects.all().order_by('-estado', 'institucion')   
    

class InstitucionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Institucion
    template_name = 'institucion/institucion_form.html'
    form_class = InstitucionForm
    success_url = reverse_lazy('institucion:institucion_list')
    context_object_name = 'institucion'
    login_url = 'core:login'
    permission_required = 'institucion.change_institucion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def form_valid(self, form):
        form.instance.institucion = form.cleaned_data['institucion']
        form.instance.tipo_institucion = form.cleaned_data['tipo_institucion']
        return super().form_valid(form)


class InstitucionDetailView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'institucion/institucion_detail.html'  # Tu template
    login_url = 'core:login'
    permission_required = 'institucion.view_institucion'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Obtiene el pk desde la URL
        institucion = get_object_or_404(Institucion, pk=pk)
        context['institucion'] = institucion
        return context

    
# @login_required(login_url='core:login')
# @permission_required('institucion.delete_institucion', login_url='core:login', raise_exception=True)
# def desactivar_institucion(request, pk):
#     institucion = get_object_or_404(Institucion, pk=pk)
#     institucion.estado = False
#     institucion.save()
#     messages.success(request, "Institución desactivada correctamente.")
#     return redirect('institucion:institucion_list')


@login_required(login_url='core:login')
@permission_required('institucion.add_institucion', login_url='core:login', raise_exception=True)
def listar_institucion(request):
    instituciones = Institucion.objects.filter(estado=True).order_by('institucion')
    medio_id = request.GET.get("medio_id")   # <-- aquí el fix
    next_url = request.GET.get("next")       # para redirigir después
    
    return render(request, "institucion/institucion_agregar_expediente.html",{ 
        "instituciones": instituciones,
        "medio_id": medio_id,
        "next_url": next_url,   # lo mandamos al template
    })


@login_required(login_url='core:login')
@permission_required('institucion.add_institucion', login_url='core:login', raise_exception=True)
def listar_institucion_by_id(request):
    instituciones = Institucion.objects.filter(estado=True).order_by('institucion')
    next_url = request.GET.get("next")       # para redirigir después
    expediente_id = request.GET.get("expediente_id")   # <--- ESTA LÍNEA ES CLAVE

    return render(request, "institucion/institucion_agregar_expediente_by_id.html",{ 
        "instituciones": instituciones,
        "next_url": next_url,
        "expediente_id": expediente_id,   # <--- ASEGÚRATE DE PASARLO AL TEMPLATE
    })



@login_required(login_url='core:login')
@permission_required('institucion.delete_institucion', login_url='core:login', raise_exception=True)
def desactivar_institucion(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    if institucion.estado:
        institucion.estado = False
        institucion.save()
        messages.success(request, "Institución desactivada correctamente.")
        return redirect('institucion:institucion_list')
    else:
        institucion.estado = True
        institucion.save()
        messages.success(request, "Institución activada correctamente.")
        return redirect('institucion:institucion_list')
    # Si es GET, muestra confirmación
    #return render(request, "institucion/confirmar_desactivacion.html", {"institucion": institucion})

