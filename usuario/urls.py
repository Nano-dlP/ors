# cuentas/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import PerfilUsuarioUpdateView, CambiarContrasenaView, blocked_ips_list, unblock_ip_view, RecuperarPasswordView, ResetearPasswordUsuarioView
from django.urls import reverse_lazy

app_name = 'usuario'

urlpatterns = [
    path('perfil/', PerfilUsuarioUpdateView.as_view(), name='editar_perfil'),
    path('cambiar-contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', success_url=reverse_lazy('usuario:password_reset_done')), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', success_url=reverse_lazy('usuario:password_reset_complete')), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    # Rutas accesibles sólo desde staff (se recomienda incluir estas rutas bajo /admin/ o
    # protegerlas con staff_member_required como hacemos en las vistas)
    path("admin/blocked-ips/", blocked_ips_list, name="blocked_ips_list"),
    path("admin/blocked-ips/unblock/<str:ip>/", unblock_ip_view, name="blocked_ips_unblock"),

    path('recuperar-contrasena/', RecuperarPasswordView.as_view(), name='recuperar_contrasena'),
    path('resetear-password/<int:user_id>/', ResetearPasswordUsuarioView.as_view(), name='resetear_password'),
]
