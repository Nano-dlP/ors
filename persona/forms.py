from django import forms
from .models import Persona




class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'tipo_documento', 'numero_documento', 'nombre', 'apellido', 'fecha_nacimiento',
            'genero', 'telefono', 'email', 'direccion_calle', 'direccion_numero',
            'direccion_piso', 'direccion_depto', 'localidad', 'ciudad_nacimiento',
            'nivel_educativo', 'ocupacion', 'posee_cobertura_salud', 'cobertura_salud',
            'posee_grupo_apoyo', 'grupo_apoyo', 
            'administra_recursos', 'carnet_discapacidad', 'situacion_habitacional',
            'observaciones', 'estado', 'carnet_unico_discapacidad',

            # 'derecho_seguridad_social', Este campo se eliminó del formulario
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_calle': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_numero': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_piso': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'direccion_depto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'localidad': forms.Select(attrs={
                                            'class': 'form-control form-control-sm select2-localidad',
                                            'id': 'id_localidad'
                                            }),
            'ciudad_nacimiento': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            
            'posee_cobertura_salud': forms.CheckboxInput(attrs={
                                                                'class': 'form-check-input',
                                                                'style': """transform: scale(1.5); 
                                                                            cursor: pointer; 
                                                                            box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); 
                                                                            border: 1px solid rgba(128, 128, 128, 1);"""}),
            'cobertura_salud': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            
            'posee_grupo_apoyo': forms.CheckboxInput(attrs={
                                                            'class': 'form-check-input',
                                                            'style': """transform: scale(1.5); 
                                                                        cursor: pointer; 
                                                                        box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); 
                                                                        border: 1px solid rgba(128, 128, 128, 1);"""}),
            'grupo_apoyo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            
            #'derecho_seguridad_social': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            
            'administra_recursos': forms.CheckboxInput(attrs={
                                                            'class': 'form-check-input',
                                                            'style': """transform: scale(1.5); 
                                                                        cursor: pointer; 
                                                                        box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); 
                                                                        border: 1px solid rgba(128, 128, 128, 1);"""}),
            
            'carnet_discapacidad': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'situacion_habitacional': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'estado': forms.CheckboxInput(attrs={
                                                'class': 'form-check-input',
                                                'style': """transform: scale(1.5); 
                                                            cursor: pointer; 
                                                            box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); 
                                                            border: 1px solid rgba(128, 128, 128, 1);"""}), 

            'carnet_unico_discapacidad': forms.CheckboxInput(attrs={
                                                'class': 'form-check-input',
                                                'style': """transform: scale(1.5); 
                                                            cursor: pointer; 
                                                            box-shadow: 0 0 0 1px rgba(128, 128, 128, 0.5); 
                                                            border: 1px solid rgba(128, 128, 128, 1);"""}),                                                            
        }
        labels = {
            'tipo_documento': 'Tipo de documento',
            'numero_documento': 'Número de documento',
            'nombre': 'Nombre(s)',
            'apellido': 'Apellido(s)',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'direccion_calle': 'Calle',
            'direccion_numero': 'Número',
            'direccion_piso': 'Piso',
            'direccion_depto': 'Depto.',
            'localidad': 'Localidad',
            'ciudad_nacimiento': 'Ciudad de nacimiento',
            'nivel_educativo': 'Nivel educativo',
            'ocupacion': 'Ocupación',
            'posee_cobertura_salud': '¿Tiene cobertura de salud?',
            'cobertura_salud': 'Cobertura de salud',
            'posee_grupo_apoyo': '¿Tiene grupo de apoyo?',
            'grupo_apoyo': 'Grupo de apoyo',
            #'derecho_seguridad_social': 'Derechos de seguridad social', Este campo se eliminó del formulario
            'administra_recursos': '¿Administra recursos?',
            'carnet_discapacidad': 'Diagnóstico consignado', # Se cambió la etiqueta Carnet de discapacidad por Diagnóstico consignado
            'situacion_habitacional': 'Situación habitacional',
            'observaciones': 'Observaciones',
            'estado': 'Estado',
            'carnet_unico_discapacidad': '¿Posee certificado único de discapacidad?', # Se cambió la etiqueta Carnet único de discapacidad por ¿Posee certificado único de discapacidad?    
        }
        


    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get("numero_documento")
        # Excluye el propio registro si está editando
        qs = Persona.objects.filter(numero_documento=numero_documento)
        if self.instance.pk:  # Si está editando (el objeto tiene pk)
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("⚠️ La persona con este DNI ya se encuentra registrada.")
        return numero_documento


    def clean(self):
        cleaned_data = super().clean()

        # Validación relacionada a campos booleanos
        if cleaned_data.get("posee_cobertura_salud") and not cleaned_data.get("cobertura_salud"):
            self.add_error("cobertura_salud", "Debe indicar la cobertura de salud si posee una.")

        if cleaned_data.get("posee_grupo_apoyo") and not cleaned_data.get("grupo_apoyo"):
            self.add_error("grupo_apoyo", "Debe indicar el grupo de apoyo si posee uno.")

        # Transformación de valores de texto
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                if field_name == 'email':
                    cleaned_data[field_name] = value.lower()  # Email en minúsculas
                elif field_name == 'observaciones':
                    cleaned_data[field_name] = value  # Observaciones sin alterar
                else:
                    cleaned_data[field_name] = value.upper()  # Todo lo demás en mayúsculas

        return cleaned_data