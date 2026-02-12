import datetime
from django import forms
from .models import Intervencion, TipoIntervencion
from expediente.models import Expediente
from profesional.models import Profesional

class IntervencionForm(forms.Form):
    expediente = forms.ModelChoiceField(
        queryset=Expediente.objects.all(), 
        widget=forms.Select(attrs={'class': "form-select d-none"}),  # oculto en UI
        required=True,
        label="Expediente"
    )
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Profesional"
    )
    tipo_intervencion = forms.ModelChoiceField(
        queryset=TipoIntervencion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de intervención"
    )
    fecha_intervencion = forms.DateField(
        initial=datetime.date.today,
        label="Fecha de intervención",  # <-- Debe ir aquí
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control form-control-sm',
                'type': 'date',
            }
        ),
        input_formats=['%Y-%m-%d']
)

    observacion = forms.CharField(
        label="Observaciones",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    def save(self):
        data = self.cleaned_data
        intervencion = Intervencion(
            expediente=data['expediente'],
            profesional=data['profesional'],
            tipo_intervencion=data['tipo_intervencion'],
            fecha_intervencion=data['fecha_intervencion'],
            observacion=data['observacion']
        )
        intervencion.save()
        return intervencion


class IntervencionCreateForm(forms.ModelForm):
    class Meta:
        model = Intervencion
        fields = ['expediente', 'profesional', 'tipo_intervencion', 'fecha_intervencion', 'observacion']
        widgets = {
            'expediente': forms.Select(attrs={'class': "form-select d-none"}),  # oculto en UI
            'profesional': forms.Select(attrs={'class': 'form-control'}),
            'tipo_intervencion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_intervencion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control form-control-sm',
                    'type': 'date',
                }
            ),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'expediente': "Expediente",
            'profesional': "Profesional",
            'tipo_intervencion': "Tipo de intervención",
            'fecha_intervencion': "Fecha de intervención",
            'observacion': "Observaciones",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['expediente'].disabled = True
        self.fields['fecha_intervencion'].input_formats = ['%Y-%m-%d']
        self.fields['observacion'].widget.attrs['placeholder'] = 'Ingrese observaciones aquí...'