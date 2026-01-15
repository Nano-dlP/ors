from django import forms
from .models import Internacion


class InternacionForm(forms.ModelForm):
    class Meta:
        model = Internacion
        fields = [
            'expediente_institucion',
            'fecha_internacion',
            'fecha_alta',
            'motivo_internacion',
            'motivo_alta',
            'tipo_internacion',
            'requisitos',
            'intento_suicidio',
            'modalidad_suicidio',
            'posee_adiccion',
            'tipo_adiccion',
            'fecha_cumplimiento',
            'observaciones',
        ]
        widgets = {
            'expediente_institucion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'fecha_internacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'fecha_alta': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'motivo_internacion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'motivo_alta': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'tipo_internacion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            #'requisitos': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ingrese requisitos...'}),
            'intento_suicidio': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': """transform: scale(1.5); cursor: pointer; box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); border: 1px solid rgba(128, 128, 128, 1);"""
            }),
            'modalidad_suicidio': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'posee_adiccion': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': """transform: scale(1.5); cursor: pointer; box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); border: 1px solid rgba(128, 128, 128, 1);"""
            }),
            'tipo_adiccion': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'fecha_cumplimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'expediente_institucion': 'Expediente Institución',
            'fecha_internacion': 'Fecha de ingreso',
            'fecha_alta': 'Fecha de externación o derivación',
            'motivo_internacion': 'Motivo de internación',
            'motivo_alta': 'Motivo de alta',
            'tipo_internacion': 'Tipo de internación',
            #'requisitos': 'Requisitos',
            'intento_suicidio': 'Intento de suicidio',
            'modalidad_suicidio': 'Modalidad de suicidio',
            'posee_adiccion': 'Consumo problemático',
            'tipo_adiccion': 'Tipo de adicción',
            'fecha_cumplimiento': 'Fecha de cumplimiento',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expediente_institucion'].widget = forms.HiddenInput()

        # ✅ Asegurar formato de fechas al editar
        for campo in ['fecha_internacion', 'fecha_alta', 'fecha_cumplimiento']:
            self.fields[campo].input_formats = ['%Y-%m-%d']

        # ✅ Bloquear edición del expediente al modificar
        if self.instance and self.instance.pk:
            self.fields['expediente_institucion'].disabled = True    

    # --- Validaciones personalizadas ---
    def clean_fecha_alta(self):
        fecha_internacion = self.cleaned_data.get('fecha_internacion')
        fecha_alta = self.cleaned_data.get('fecha_alta')
        if fecha_internacion and fecha_alta and fecha_alta < fecha_internacion:
            raise forms.ValidationError("⚠️ La fecha de alta no puede ser anterior a la fecha de internación.")
        return fecha_alta

    def clean_fecha_cumplimiento(self):
        fecha_cumplimiento = self.cleaned_data.get('fecha_cumplimiento')
        fecha_internacion = self.cleaned_data.get('fecha_internacion')
        fecha_alta = self.cleaned_data.get('fecha_alta')

        if fecha_cumplimiento:
            if fecha_internacion and fecha_cumplimiento < fecha_internacion:
                raise forms.ValidationError("⚠️ La fecha de cumplimiento no puede ser anterior a la internación.")
            if fecha_alta and fecha_cumplimiento < fecha_alta:
                raise forms.ValidationError("⚠️ La fecha de cumplimiento no puede ser anterior a la alta.")
        return fecha_cumplimiento
