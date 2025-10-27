from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth import password_validation

User = get_user_model()

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'dni', 'telefono', 'direccion', 'localidad', 'sede', 'foto_perfil']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    #def clean_dni(self):
    #    dni = self.cleaned_data.get('dni')
    #    if not dni:
    #        raise ValidationError("El campo DNI no puede estar vacío.")
        
        # Si es edición (el usuario ya existe), excluimos su propio ID
    #    if CustomUser.objects.filter(dni=dni).exclude(id=self.instance.id).exists():
    #        raise ValidationError("Ya existe un usuario con ese DNI.")
        
    #    return dni


class RecuperarPasswordForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")


class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña actual"}),
    )
    nueva_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Nueva contraseña"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirmar_password = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirmar nueva contraseña"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva = cleaned_data.get("nueva_password")
        confirmar = cleaned_data.get("confirmar_password")
        if nueva and confirmar and nueva != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        password_validation.validate_password(nueva)
        return cleaned_data