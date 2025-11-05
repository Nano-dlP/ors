

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from urllib.parse import urlencode
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from .models import Persona
from .forms import PersonaForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required


class PersonaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Persona
    template_name = "persona/persona_form.html"
    form_class = PersonaForm
    success_url = reverse_lazy('persona:persona_list')
    context_object_name = 'persona'
    login_url = 'core:login'
    permission_required = 'persona.puede_crear_persona'  # reemplaza 'persona' por tu app_label
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    # Opcional: manejar 403 de forma personalizada
    def handle_no_permission(self):
        return render(self.request, 'core/403.html', status=403)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)

        next_url = self.request.GET.get('next')
        if next_url:
            query_string = urlencode({'persona_id': self.object.pk})
            return HttpResponseRedirect(f'{next_url}?{query_string}')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')  # 🔹 pasa el parámetro al template
        return context



class PersonaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Persona
    template_name = "persona/persona_list.html"
    context_object_name = 'personas'
    login_url = 'core:login'
    permission_required = 'persona.puede_ver_persona'  # reemplaza 'persona' por tu app_label
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    
    def get_queryset(self):
        # Solo personas activas
        return Persona.objects.filter().order_by('apellido', 'nombre')
    


class PersonaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Persona
    template_name = 'persona/persona_form.html'
    form_class = PersonaForm
    success_url = reverse_lazy('persona:persona_list')
    context_object_name = 'personas'
    login_url = 'core:login'
    permission_required = 'persona.puede_editar_persona'  # reemplaza 'persona' por tu app_label
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)



class PersonaDetailView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'persona/persona_detail.html'  # Tu template
    login_url = 'core:login'
    permission_required = 'persona.puede_ver_persona'  # reemplaza 'persona' por tu app_label
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Obtiene el pk desde la URL
        persona = get_object_or_404(Persona, pk=pk)
        context['persona'] = persona
        return context
    

@login_required(login_url='core:login')
@permission_required('persona.puede_ver_persona', login_url='core:login', raise_exception=True)
def persona_list(request):
    personas = Persona.objects.filter(estado=True).order_by('apellido', 'nombre')
    medio_id = request.GET.get("medio_id")   # <-- aquí el fix
    next_url = request.GET.get("next")       # para redirigir después
    return render(request, "persona/persona_agregar_expediente.html", {
        "personas": personas,
        "medio_id": medio_id,
        "next_url": next_url,   # lo mandamos al template
    })


@login_required(login_url='core:login')
@permission_required('persona.puede_ver_persona', login_url='core:login', raise_exception=True)
def agregar_persona_expediente(request):
    personas = Persona.objects.filter(estado=True).order_by('apellido', 'nombre')
    next_url = request.GET.get("next") or reverse_lazy('expediente:expediente_list')  # valor por defecto

    return render(request, "expediente/expediente_persona_form.html", {
        "personas": personas,
        "next_url": next_url,  # 👈 usar "next" en vez de "next_url"
    })

@login_required(login_url='core:login')
#@permission_required('persona.puede_desactivar_persona, persona.puede_activar_persona', login_url='core:login', raise_exception=True)
def desactivar_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if persona.estado:
        persona.estado = False
        persona.save()
        messages.success(request, "Persona desactivada correctamente.")
        return redirect('persona:persona_list')
    else:
        persona.estado = True
        persona.save()
        messages.success(request, "Persona activada correctamente.")
        return redirect('persona:persona_list')