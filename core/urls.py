
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import ProvinciaListView, IndexView, ProvinciaCreate
from . import views

app_name = 'core'

urlpatterns = [
    path('provincia/', ProvinciaListView.as_view(), name='provincia_list'),
    path('', IndexView.as_view(), name='index'),
    path('provincia_nuevo/', ProvinciaCreate.as_view(), name='provincia_create'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('localidades/', views.localidad_autocomplete, name='localidad-autocomplete'),

    # Password reset - nombres estándar de Django (recomendado)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', success_url=reverse_lazy('core:password_reset_done')), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', success_url=reverse_lazy('core:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    
]
