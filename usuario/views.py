# cuentas/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, FormView
from .forms import RecuperarPasswordForm, CambiarPasswordForm
from django.contrib.auth import update_session_auth_hash
from .utils import reset_user_password, validate_password_strength
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PerfilUsuarioForm
from django.contrib.auth import get_user_model
# cuentas/views.py (agrega esto también)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from .utils import generate_random_password, enviar_password_por_email


import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.cache import cache

from .blocked_ip_helpers import get_blocked_ips, remove_blocked_ip


logger = logging.getLogger(__name__)

BLOCKED_KEY_PREFIX = "blocked_ip:"




User = get_user_model()

class PerfilUsuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = PerfilUsuarioForm
    template_name = 'usuario/usuario_edit.html'
    success_url = reverse_lazy('usuario:editar_perfil')  # redirige a sí misma
    login_url = reverse_lazy('core:login')
    permission_required = 'auth.change_user'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_object(self, queryset=None):
        return self.request.user  # el usuario logueado

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)



#class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, PasswordChangeView):
#    form_class = PasswordChangeForm
#    template_name = 'usuario/usuario_contrasenia.html'
#    success_url = reverse_lazy('usuario:editar_perfil')
#    login_url = reverse_lazy('login')
#    permission_required = 'auth.change_user'
#    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

#    def form_valid(self, form):
#        messages.success(self.request, "Contraseña actualizada correctamente.")
#        return super().form_valid(form)
    
    
    
@staff_member_required
def blocked_ips_list(request):
    """
    Vista protegida para listar IPs bloqueadas. Si no es posible listar (por ejemplo
    no hay redis), muestra mensaje informando que el listado no está disponible.
    """
    try:
        ips = get_blocked_ips()
        can_list = ips is not None
    except Exception:
        logger.exception("Error obteniendo blocked ips")
        ips = None
        can_list = False

    context = {
        "blocked_ips": ips or [],
        "can_list": can_list,
    }
    return render(request, "admin/blocked_ips.html", context)


@staff_member_required
@require_http_methods(["POST"])
def unblock_ip_view(request, ip):
    """
    Desbloquea la IP: elimina la clave blocked_ip:<ip> y la quita del set listable.
    """
    try:
        remove_blocked_ip(ip)
        messages.success(request, f"IP {ip} desbloqueada correctamente.")
    except Exception:
        logger.exception("Error desbloqueando IP %s", ip)
        messages.error(request, f"No se pudo desbloquear la IP {ip}. Revisa logs.")
    # Redirigir de vuelta a la lista
    return redirect(reverse("admin:blocked_ips_list"))


class RecuperarPasswordView(FormView):
    template_name = "usuario/recuperar_password.html"
    form_class = RecuperarPasswordForm
    success_url = reverse_lazy("core:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        ok, msg = reset_user_password(email)
        if ok:
            messages.success(self.request, msg)
        else:
            messages.error(self.request, msg)
        return super().form_valid(form)
    

class CambiarContrasenaView(LoginRequiredMixin, FormView):
    template_name = "usuario/cambiar_contrasena.html"
    form_class = CambiarPasswordForm
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        user = self.request.user
        actual = form.cleaned_data["password_actual"]
        nueva = form.cleaned_data["nueva_password"]

        # 1️⃣ Verificar contraseña actual sin alterar sesión
        if not user.check_password(actual):
            messages.error(self.request, "La contraseña actual es incorrecta.")
            return self.render_to_response(self.get_context_data(form=form))

        # 2️⃣ Validar seguridad de la nueva contraseña
        es_valida, mensaje = validate_password_strength(nueva)
        if not es_valida:
            messages.error(self.request, f"La nueva contraseña no es segura: {mensaje}")
            return self.render_to_response(self.get_context_data(form=form))

        # 3️⃣ Guardar y mantener la sesión
        user.set_password(nueva)
        user.save()
        update_session_auth_hash(self.request, user)  # mantiene sesión activa

        messages.success(self.request, "Tu contraseña se cambió correctamente.")
        return super().form_valid(form)

#class CambiarContrasenaView(LoginRequiredMixin, PermissionRequiredMixin, PasswordChangeView):
#    form_class = PasswordChangeForm
#    template_name = 'usuario/usuario_contrasenia.html'
#    success_url = reverse_lazy('usuario:editar_perfil')
#    login_url = reverse_lazy('login')
#    permission_required = 'auth.change_user'
#    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

#    def form_valid(self, form):
#        messages.success(self.request, "Contraseña actualizada correctamente.")
#        return super().form_valid(form)

class ResetearPasswordUsuarioView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'
    raise_exception = True  # Devuelve 403 si no tiene permiso

    def get(self, request, user_id):
        usuario = get_object_or_404(User, id=user_id)
        nueva_password = generate_random_password()
        usuario.set_password(nueva_password)
        usuario.save()

        try:
            enviar_password_por_email(usuario, nueva_password)
            messages.success(request, f"Contraseña restablecida y enviada a {usuario.email}.")
        except Exception as e:
            messages.warning(request, f"Contraseña cambiada, pero no se pudo enviar el correo: {e}")

        return redirect("admin:index")
