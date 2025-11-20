# Importamos algunas librerías necesarias para trabajar con fechas y vistas en Django
import datetime
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy

from django.http import JsonResponse
from django.db.models import Q


from expediente.models import Expediente


import logging

# Mezclas para controlar permisos y autenticación de usuarios
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

# Vistas genéricas para mostrar listas y editar objetos
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Funciones para redirigir usuarios y obtener objetos de la base de datos
from django.shortcuts import redirect

# Importamos los formularios que se usarán en las vistas
from .forms import DemandaEspontanea, MedioIngresoForm, OficioForm, SecretariaForm, ExpedienteInstitucionForm, ExpedientePersonaForm

# Importamos los modelos (tablas) que usaremos para guardar y consultar información
from .models import Expediente, ExpedientePersona, Rol, ExpedienteInstitucion, ExpedienteDocumento, MedioIngreso
from persona.models import Persona
from institucion.models import Institucion

# Funciones para renderizar páginas y mostrar mensajes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ExpedienteDocumentoFormSet, ExpedienteDocumentoForm
from django.views import View


logger = logging.getLogger(__name__)

# Vista para listar todos los expedientes (casos)
class ExpedienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Expediente  # Usamos el modelo Expediente
    template_name = 'expediente/expediente_list.html'  # HTML que se usará para mostrar la lista
    context_object_name = 'expedientes'  # Nombre de la variable que contiene los expedientes en el HTML
    login_url = 'core:login'  # Si el usuario no está logueado, lo enviamos a esta página
    permission_required = 'expediente.view_expediente' # Permiso necesario para ver expedientes
    raise_exception = False  # Si no tiene permiso, muestra error 403

    def get_queryset(self):
        user = self.request.user

        # 🔹 Comenzamos desde el queryset base del modelo Expediente
        queryset = Expediente.objects.all().order_by('-identificador')

        # 🔹 Si el usuario tiene una sede asociada, filtramos los expedientes por esa sede
        if hasattr(user, 'sede') and user.sede:
            queryset = queryset.filter(sede=user.sede)

        return queryset


# Vista para seleccionar el medio de ingreso, primer paso para crear un expediente
class MedioIngresoSelectView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/medio_ingreso.html'
    form_class = MedioIngresoForm
    login_url = 'core:login'
    permission_required = 'expediente.view_medioingreso'
    raise_exception = False
    
    def get_initial(self):
        initial = super().get_initial()
        # Busca el medio "Demanda Espontánea"
        medio = MedioIngreso.objects.filter().first()
        if medio:
            initial['medio_ingreso'] = medio
        return initial

 
    def form_valid(self, form):
        # Esta función decide a qué formulario redirigir según el medio de ingreso elegido
        medio_ingreso_id = form.cleaned_data['medio_ingreso'].id

        if medio_ingreso_id in [1,] :
            # Si el medio es 1, redirige a crear expediente con ese medio
            return redirect('expediente:expediente_create_with_medio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [2, 3, 4, 5, 6] :
            # Si el medio es entre 2 y 6, redirige a crear expediente tipo oficio
            return redirect('expediente:expediente_create_oficio', medio_id=medio_ingreso_id)
        elif  medio_ingreso_id in [7,] :
            # Si el medio es 7, redirige a crear expediente normal
            return redirect('expediente:expediente_create', medio_id=medio_ingreso_id)
        else:
            # Si no coincide, vuelve a la selección
            return redirect('expediente:medio_ingreso_select')


# Vista que decide qué formulario mostrar para editar según el tipo de expediente
class ExpedienteUpdateDispatcherView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = False

    def get(self, request, pk):
        expediente = get_object_or_404(Expediente, pk=pk)
        medio = expediente.medio_ingreso.medio_ingreso if expediente.medio_ingreso else ""

        # Según el medio de ingreso, redirige al formulario correcto
        # Para editar cada tipo de expediente usamos las vistas ya definidas y registradas en urls.py
        # Cada tipo de expediente tiene su propia vista de edición

        medios_oficio = [
            "OFICIO POR MAIL",
            "OFICIO PAPEL",
            "DERIVACION",
            "MAIL EFECTOR",
            "COMUNICACION TELEFONICA EQUIPO TRATANTE",
        ]

        if medio == "DEMANDA ESPONTANEA":
            return redirect('expediente:demanda_espontanea_update', pk=pk)
        elif medio in medios_oficio:
            return redirect('expediente:oficio_update', pk=pk)
        elif medio == "SOLICITUD SECRETARIA EJECUTIVA (DE OFICIO)":
            return redirect('expediente:secretaria_update', pk=pk)
        else:
            # Si no reconoce el medio, muestra error
            messages.error(request, "No se pudo determinar el tipo de expediente.")
            return redirect('expediente:expediente_list')


class ExpedienteDetailDispatcherView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'core:login'
    permission_required = 'expediente.view_expediente'
    raise_exception = False
    
    def get(self, request, pk):
        expediente = get_object_or_404(Expediente, pk=pk)
        medio = expediente.medio_ingreso.medio_ingreso if expediente.medio_ingreso else ""
        print(medio)
        # Según el medio de ingreso, redirige al formulario correcto
        # Para editar cada tipo de expediente usamos las vistas ya definidas y registradas en urls.py
        # Cada tipo de expediente tiene su propia vista de edición

        medios_oficio = [
            "OFICIO POR MAIL",
            "OFICIO PAPEL",
            "DERIVACION",
            "MAIL EFECTOR",
            "COMUNICACION TELEFONICA EQUIPO TRATANTE",
        ]

        if medio == "DEMANDA ESPONTANEA":
            return redirect('expediente:demanda_espontanea_detail', pk=pk)
        elif medio in medios_oficio:
            return redirect('expediente:oficio_detail', pk=pk)
        elif medio == "SOLICITUD SECRETARIA EJECUTIVA (DE OFICIO)":
            return redirect('expediente:secretaria_detail', pk=pk)
        else:
            # Si no reconoce el medio, muestra error
            messages.error(request, "No se pudo determinar el tipo de expediente.")
            return redirect('expediente:expediente_list')

# Vista para crear expedientes del tipo "Demanda Espontanea"
# Es el expediente más común y tiene a la persona como actor principal
class DemandaEspontaneaCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expediente'
    raise_exception = False

    def get_medio_id(self):
        """Obtiene medio_id desde kwargs o GET, priorizando kwargs."""
        return self.kwargs.get('medio_id') or self.request.GET.get('medio_id')

    def get_initial(self):
        # Prepara los datos iniciales del formulario, como el medio de ingreso y la fecha
        initial = super().get_initial()
        medio_id = self.get_medio_id()
        persona_id = self.request.GET.get('persona_id')

        if medio_id:
            medio = get_object_or_404(MedioIngreso, pk=medio_id)
            initial['medio_ingreso'] = medio
            initial['fecha_creacion'] = datetime.date.today()

        if persona_id:
            try:
                initial['persona'] = Persona.objects.get(pk=persona_id)
            except Persona.DoesNotExist:
                pass    

        return initial
    

    def get_form(self, form_class=None):
        # Crea el formulario y deshabilita el campo medio_ingreso
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        # Prepara datos adicionales para la plantilla, como el formset de documentos
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=ExpedienteDocumento.objects.none()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())
        
        persona_id = self.request.GET.get('persona_id')
        if persona_id:
            context['persona_seleccionada'] = Persona.objects.filter(pk=persona_id).first()    

        # --- FIX: añade medio_id al contexto ---
        context['medio_id'] = self.get_medio_id()
        # ---------------------------------------    
        return context

    def form_valid(self, form):
        # Si el formulario es válido, crea el expediente y las relaciones necesarias
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        #if not documento_formset.is_valid():
        #    messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
        #    return self.form_invalid(form)

        persona = form.cleaned_data.get('persona')
        if not persona:
            form.add_error('persona', 'Debe seleccionar una persona')
            messages.error(self.request, "Debe seleccionar una persona para crear el expediente.")
            return self.form_invalid(form)
        

        # Extrae datos del formulario
        sede = form.cleaned_data['sede']
        fecha_creacion = form.cleaned_data['fecha_creacion']
        medio_ingreso = form.cleaned_data['medio_ingreso']
        rol = form.cleaned_data['rol']
        tipo_solicitud = form.cleaned_data['tipo_solicitud']
        estado_expediente = form.cleaned_data['estado_expediente']
        grupo_etario = form.cleaned_data['grupo_etario']
        edad_persona = form.cleaned_data['edad_persona']
        situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        resumen_intervencion = form.cleaned_data['resumen_intervencion']
        observaciones = form.cleaned_data['observaciones']


        # Crea el expediente
        expediente = Expediente.objects.create(
            sede=sede,
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,
            tipo_solicitud=tipo_solicitud,
            estado_expediente=estado_expediente,
            grupo_etario=grupo_etario,
            edad_persona=edad_persona,
            situacion_habitacional_hist=situacion_habitacional_hist,
            resumen_intervencion=resumen_intervencion,
            observaciones=observaciones,
        )

        # Relaciona la persona con el expediente
        if persona:
            try:
                ExpedientePersona.objects.create(
                    expediente=expediente,
                    persona=persona,
                    rol=rol
                )
            except Exception as e:
                messages.error(self.request, f"No se pudo registrar la persona: {e}")
                return self.form_invalid(form)

        # Guarda los documentos vinculados al expediente
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue creado correctamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Muestra mensaje si hubo errores
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)


# (Las siguientes vistas siguen la misma lógica: muestran formularios, validan datos, crean o actualizan objetos en la base de datos, y preparan datos para mostrar en el HTML. Cada clase tiene comentarios en las partes principales del flujo.)
class DemandaEspontaneaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/demanda_espontanea_form.html'
    form_class = DemandaEspontanea
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_object(self):
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        expediente = self.get_object()
        initial = super().get_initial()

        # Persona vinculada
        persona_rel = expediente.expedientepersona_expediente.first()
        # El rol viene de la relación persona_rel
        initial.update({
            'persona': persona_rel.persona if persona_rel else None,
            'sede': expediente.sede,
            'fecha_creacion': expediente.fecha_creacion,
            'medio_ingreso': expediente.medio_ingreso,
            'rol': persona_rel.rol if persona_rel else None,
            'tipo_solicitud': expediente.tipo_solicitud,
            'estado_expediente': expediente.estado_expediente,
            'grupo_etario': expediente.grupo_etario,
            'edad_persona': expediente.edad_persona,
            'situacion_habitacional_hist': expediente.situacion_habitacional_hist,
            'resumen_intervencion': expediente.resumen_intervencion,
            'observaciones': expediente.observaciones,
        })
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        expediente = self.get_object()  # obtenemos el expediente que se está editando

        form = form_class(
            user=self.request.user,
            expediente=expediente,  # 👈 pasamos la instancia al form
            **self.get_form_kwargs()
        )

        form.fields['medio_ingreso'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.get_object()

        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                queryset=expediente.documentos.all()
            )

        # Persona seleccionada para mostrar en template
        persona_rel = expediente.expedientepersona_expediente.first()
        context['persona_seleccionada'] = persona_rel.persona if persona_rel else None
        context['rol_seleccionado'] = persona_rel.rol if persona_rel else None

        # Indicar que es edición
        context['editar'] = True

        # Número de expediente
        context['numero_expediente'] = expediente.identificador  # ajustar según tu campo real
        return context

    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        # documento_formset = context['documento_formset']

        # if not documento_formset.is_valid():
        #     return self.form_invalid(form)

        # Actualizar campos del expediente
        expediente.sede = form.cleaned_data['sede']
        expediente.fecha_creacion = form.cleaned_data['fecha_creacion']
        expediente.tipo_solicitud = form.cleaned_data['tipo_solicitud']
        expediente.estado_expediente = form.cleaned_data['estado_expediente']
        expediente.grupo_etario = form.cleaned_data['grupo_etario']
        expediente.edad_persona = form.cleaned_data['edad_persona']
        expediente.situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        expediente.resumen_intervencion = form.cleaned_data['resumen_intervencion']
        expediente.observaciones = form.cleaned_data['observaciones']
        expediente.save()

        # Actualizar o crear relación con persona (versión corregida)
        persona = form.cleaned_data['persona']
        rol = form.cleaned_data['rol']

        # 1) Buscar relaciones existentes para el expediente y la persona (ignorando el rol)
        persona_qs = ExpedientePersona.objects.filter(expediente=expediente, persona=persona)

        if persona_qs.exists():
            # Tomamos la primera relación existente para esa persona y la actualizamos con el nuevo rol
            ep_obj = persona_qs.order_by('id').first()

            if ep_obj.rol != rol:
                ep_obj.rol = rol
                ep_obj.save()
                logger.info(
                    "Actualizado rol de ExpedientePersona id=%s a rol=%s (expediente=%s, persona=%s)",
                    ep_obj.pk, rol, expediente.pk, getattr(persona, 'pk', persona)
                )

            # Si hay duplicados exactos (mismas persona+expediente), los dejamos registrados para limpieza
            duplicates = persona_qs.exclude(pk=ep_obj.pk)
            if duplicates.exists():
                logger.warning(
                    "Se encontraron %d ExpedientePersona duplicadas para expediente=%s persona=%s. "
                    "Manteniendo id=%s. Considerar limpiar la DB.",
                    duplicates.count(), expediente.pk, getattr(persona, 'pk', persona), ep_obj.pk
                )
                # Opcional: eliminar duplicados automáticamente (descomentar si quieres borrar)
                # duplicates.delete()
        else:
            # No existe relación para esa persona -> crear nueva relación con el rol seleccionado
            ExpedientePersona.objects.create(expediente=expediente, persona=persona, rol=rol)
            logger.info(
                "Creada nueva ExpedientePersona expediente=%s persona=%s rol=%s",
                expediente.pk, getattr(persona, 'pk', persona), rol
            )

        # Guardar documentos (si vuelves a activarlos)
        # for documento_form in documento_formset:
        #     if documento_form.cleaned_data:
        #         documento = documento_form.save(commit=False)
        #         documento.expediente = expediente
        #         documento.save()

        messages.success(self.request, "El expediente fue actualizado correctamente.")
        return super().form_valid(form)



class DemandaEspontaneaDetailView(DetailView):
    model = Expediente
    template_name = "expediente/demanda_espontanea_detalle.html"
    context_object_name = "expediente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Documentos asociados al expediente
        context["documentos"] = ExpedienteDocumento.objects.filter(expediente=self.object)
        # Persona principal (rol=1) asociada al expediente
        persona_rel = ExpedientePersona.objects.filter(expediente=self.object, rol__pk=1).first()
        context["persona"] = persona_rel.persona if persona_rel else None
        return context



class OficioCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expediente'
    raise_exception = False

    def get_medio_id(self):
        """Obtiene medio_id desde kwargs o GET, priorizando kwargs."""
        return self.kwargs.get('medio_id') or self.request.GET.get('medio_id')

    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.get_medio_id()
        institucion_id = self.request.GET.get('institucion_id')

        # Set medio_ingreso from URL/GET only once (not in POST)
        if medio_id:
            medio = get_object_or_404(MedioIngreso, pk=medio_id)
            initial['medio_ingreso'] = medio
            initial['fecha_creacion'] = datetime.date.today()

        if institucion_id:
            try:
                initial['institucion'] = Institucion.objects.get(pk=institucion_id)
            except Institucion.DoesNotExist:
                pass

        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        # Campo de medio_ingreso: solo lectura visual, pero editable internamente.
        form.fields['medio_ingreso'].disabled = True
        form.fields['medio_ingreso'].widget.attrs['style'] = 'pointer-events: none; background-color: #f8f9fa;'  # Estilo visual
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=ExpedienteDocumento.objects.none()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())

        institucion_id = self.request.GET.get('institucion_id')
        if institucion_id:
            context['institucion_seleccionada'] = Institucion.objects.filter(pk=institucion_id).first()

        # --- FIX: añade medio_id al contexto ---
        context['medio_id'] = self.get_medio_id()
        # ---------------------------------------
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        #if not documento_formset.is_valid():
        #    messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
        #    return self.form_invalid(form)

        institucion = form.cleaned_data.get('institucion')
        if not institucion:
            form.add_error('institucion', 'Debe seleccionar una institución')
            messages.error(self.request, "Debe seleccionar una institución para crear el expediente.")
            return self.form_invalid(form)

        # Obtiene el medio_ingreso SIEMPRE desde la URL o GET, no del form.cleaned_data 
        medio_id = self.get_medio_id()
        medio_ingreso = get_object_or_404(MedioIngreso, pk=medio_id)

        # Obtiene el resto normalmente
        sede = form.cleaned_data.get('sede')
        fecha_creacion = form.cleaned_data.get('fecha_creacion')
        fecha_de_juzgado = form.cleaned_data.get('fecha_de_juzgado')
        fecha_de_recepcion = form.cleaned_data.get('fecha_de_recepcion')
        expediente_fisico = form.cleaned_data.get('expediente_fisico')
        cuij = form.cleaned_data.get('cuij')
        clave_sisfe = form.cleaned_data.get('clave_sisfe')
        tipo_solicitud = form.cleaned_data.get('tipo_solicitud')
        estado_expediente = form.cleaned_data.get('estado_expediente')
        grupo_etario = form.cleaned_data.get('grupo_etario')
        edad_persona = form.cleaned_data.get('edad_persona')
        situacion_habitacional_hist = form.cleaned_data.get('situacion_habitacional_hist')
        rol = form.cleaned_data['rol']
        tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        resumen_intervencion = form.cleaned_data.get('resumen_intervencion')
        observaciones = form.cleaned_data.get('observaciones')

        #try:
        #    rol = Rol.objects.get(pk=2)
        #except Rol.DoesNotExist:
        #    form.add_error(None, 'El rol predeterminado no existe.')
        #    return self.form_invalid(form)

        # Crea el expediente con el medio_ingreso correcto
        expediente = Expediente.objects.create(
            sede=sede,
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,  # <-- SIEMPRE desde URL o GET
            fecha_de_juzgado=fecha_de_juzgado,
            fecha_de_recepcion=fecha_de_recepcion,
            expediente_fisico=expediente_fisico,
            cuij=cuij,
            clave_sisfe=clave_sisfe,
            tipo_solicitud=tipo_solicitud,
            estado_expediente=estado_expediente,
            grupo_etario=grupo_etario,
            edad_persona=edad_persona,
            situacion_habitacional_hist=situacion_habitacional_hist,
            tipo_patrocinio=tipo_patrocinio,
            resumen_intervencion=resumen_intervencion,
            observaciones=observaciones
        )

        # Relación con institución
        if institucion:
            try:
                ExpedienteInstitucion.objects.create(
                    expediente=expediente,
                    institucion=institucion,
                    rol=rol
                )
            except Exception as e:
                messages.error(self.request, f"No se pudo registrar la institución: {e}")
                return self.form_invalid(form)

        #Vincula documentos
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue creado correctamente.")
        return redirect(reverse('expediente:expediente_institucion_create_by_id', kwargs={'expediente_id': expediente.id})
    )

    def form_invalid(self, form):
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)
    
    

class OficioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/oficio_form.html'
    form_class = OficioForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_object(self):
        # Obtiene el expediente por la pk de la URL
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        # Carga los datos existentes del expediente en el formulario
        expediente = self.get_object()
        initial = super().get_initial()

        # Institución vinculada
        institucion_rel = expediente.expedienteinstitucion_expediente.first()

        # El rol viene de la relación institucion_rel
        initial.update({
            'institucion': institucion_rel.institucion if institucion_rel else None,
            'fecha_creacion': expediente.fecha_creacion,
            'sede': expediente.sede,
            'medio_ingreso': expediente.medio_ingreso,
            'fecha_de_juzgado': expediente.fecha_de_juzgado,
            'fecha_de_recepcion': expediente.fecha_de_recepcion,
            'expediente_fisico': expediente.expediente_fisico,
            'cuij': expediente.cuij,
            'clave_sisfe': expediente.clave_sisfe,
            'tipo_solicitud': expediente.tipo_solicitud,
            'estado_expediente': expediente.estado_expediente,
            'grupo_etario': expediente.grupo_etario,
            'edad_persona': expediente.edad_persona,
            'situacion_habitacional_hist': expediente.situacion_habitacional_hist,
            'rol': institucion_rel.rol if institucion_rel else None,
            'tipo_patrocinio': expediente.tipo_patrocinio,
            'resumen_intervencion': expediente.resumen_intervencion,
            'observaciones': expediente.observaciones,
        })
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        expediente = self.get_object()  # obtenemos el expediente que se está editando

        form = form_class(
            user=self.request.user,
            expediente=expediente,  # 👈 pasamos la instancia al form
            **self.get_form_kwargs()
        )

        form.fields['medio_ingreso'].disabled = True
        return form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.get_object()

        
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                queryset=expediente.documentos.all()
            )

        # Institución seleccionada para mostrar en template
        institucion_rel = expediente.expedienteinstitucion_expediente.first()
        context['institucion_seleccionada'] = institucion_rel.institucion if institucion_rel else None
        context['rol_seleccionado'] = institucion_rel.rol if institucion_rel else None

        # Indicar que es edición
        context['editar'] = True

        # Número de expediente
        context['numero_expediente'] = expediente.identificador  # ajustar según tu campo real
        return context

    def form_valid(self, form):
        expediente = self.get_object()
        context = self.get_context_data()
        #documento_formset = context['documento_formset']

        #if not documento_formset.is_valid():
        #    messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
        #    return self.form_invalid(form)

        institucion_obj = form.cleaned_data.get('institucion')
        
        if not institucion_obj:
            form.add_error('institucion', 'Debe seleccionar una institución')
            messages.error(self.request, "Debe seleccionar una institución para actualizar el expediente.")
            return self.form_invalid(form)

        # Actualiza los datos del expediente
        expediente.sede = form.cleaned_data.get('sede')
        expediente.fecha_creacion = form.cleaned_data.get('fecha_creacion')
        expediente.medio_ingreso = form.cleaned_data.get('medio_ingreso')
        expediente.fecha_de_juzgado = form.cleaned_data.get('fecha_de_juzgado')
        expediente.fecha_de_recepcion = form.cleaned_data.get('fecha_de_recepcion')
        expediente.expediente_fisico = form.cleaned_data.get('expediente_fisico')
        expediente.cuij = form.cleaned_data.get('cuij')
        expediente.clave_sisfe = form.cleaned_data.get('clave_sisfe')
        expediente.tipo_solicitud = form.cleaned_data.get('tipo_solicitud')
        expediente.estado_expediente = form.cleaned_data.get('estado_expediente')
        expediente.grupo_etario = form.cleaned_data.get('grupo_etario')
        expediente.edad_persona = form.cleaned_data.get('edad_persona')
        expediente.situacion_habitacional_hist = form.cleaned_data.get('situacion_habitacional_hist')
        expediente.tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        expediente.resumen_intervencion = form.cleaned_data.get('resumen_intervencion')
        expediente.observaciones = form.cleaned_data.get('observaciones')
        expediente.save()

        # Actualiza o crea relación con institución (versión robusta)
        rol = form.cleaned_data.get('rol')

        # Buscar relación exacta por expediente + institución
        exact_qs = ExpedienteInstitucion.objects.filter(
            expediente=expediente, institucion=institucion_obj
        )

        if exact_qs.exists():
            # Tomamos la primera relación encontrada y actualizamos el rol si cambió
            ei_obj = exact_qs.order_by('id').first()
            if ei_obj.rol != rol:
                ei_obj.rol = rol
                ei_obj.save()
                logger.info(
                    "Actualizado rol de ExpedienteInstitucion id=%s a rol=%s (expediente=%s, institucion=%s)",
                    ei_obj.pk, rol, expediente.pk, getattr(institucion_obj, 'pk', institucion_obj)
                )

            # Si hay duplicados exactos (mismas institucion+expediente), los dejamos registrados para limpieza
            duplicates = exact_qs.exclude(pk=ei_obj.pk)
            if duplicates.exists():
                logger.warning(
                    "Se encontraron %d ExpedienteInstitucion duplicadas para expediente=%s institucion=%s. "
                    "Manteniendo id=%s. Considerar limpiar la DB.",
                    duplicates.count(), expediente.pk, getattr(institucion_obj, 'pk', institucion_obj), ei_obj.pk
                )
                # Opcional: eliminar duplicados automáticamente (descomentar si quieres borrar)
                # duplicates.delete()
        else:
            # No existe relación exacta -> crear nueva relación con el rol seleccionado
            ExpedienteInstitucion.objects.create(expediente=expediente, institucion=institucion_obj, rol=rol)
            logger.info(
                "Creada nueva ExpedienteInstitucion expediente=%s institucion=%s rol=%s",
                expediente.pk, getattr(institucion_obj, 'pk', institucion_obj), rol
            )

        # Actualiza documentos vinculados al expediente (si vuelves a activarlos)
        # for documento_form in documento_formset:
        #     if documento_form.cleaned_data.get('archivo'):
        #         documento = documento_form.save(commit=False)
        #         documento.expediente = expediente
        #         documento.save()

        messages.success(self.request, "El expediente fue actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, "Hubo errores al actualizar el expediente. Verifique los campos.")
        return super().form_invalid(form)



class OficioDetailView(DetailView):
    model = Expediente
    template_name = "expediente/oficio_detalle.html"
    context_object_name = "expediente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Documentos asociados al expediente
        context["documentos"] = ExpedienteDocumento.objects.filter(expediente=self.object)
        # Institución principal (rol=2) asociada al expediente
        institucion_rel = ExpedienteInstitucion.objects.filter(expediente=self.object, rol__pk=2).first()
        context["institucion"] = institucion_rel.institucion if institucion_rel else None
        return context



class SecretariaCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/secretaria_form.html'
    form_class = SecretariaForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expediente'
    raise_exception = False  # devuelve 403 Forbidden si no tiene permiso

    def get_medio_id(self):
        """Obtiene medio_id desde kwargs o GET, priorizando kwargs."""
        return self.kwargs.get('medio_id') or self.request.GET.get('medio_id')


    def get_initial(self):
        initial = super().get_initial()
        medio_id = self.get_medio_id()

        # Medio de ingreso
        if medio_id:
            medio = get_object_or_404(MedioIngreso, pk=medio_id)
            initial['medio_ingreso'] = medio
            initial['fecha_creacion'] = datetime.date.today()

        return initial

    #Función del formulario para obtener usuario y medio de ingreso
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(user=self.request.user, **self.get_form_kwargs())
        form.fields['medio_ingreso'].disabled = True
        form.fields['medio_ingreso'].widget.attrs['style'] = 'pointer-events: none; background-color: #f8f9fa;'  # Estilo visual
        return form
    
    def get_context_data(self, **kwargs):
        # Prepara datos adicionales para la plantilla, como el formset de documentos
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, self.request.FILES, queryset=ExpedienteDocumento.objects.none()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())
        
        # --- FIX: añade medio_id al contexto ---
        context['medio_id'] = self.get_medio_id()
        # ---------------------------------------

        return context

    def form_valid(self, form):
        # Si el formulario es válido, crea el expediente y las relaciones necesarias
        context = self.get_context_data()
        documento_formset = context['documento_formset']

        #if not documento_formset.is_valid():
        #    messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
        #    return self.form_invalid(form)

        fecha_de_juzgado = form.cleaned_data['fecha_de_juzgado']
        fecha_de_recepcion = form.cleaned_data['fecha_de_recepcion']
        sede = form.cleaned_data['sede']
        fecha_creacion = form.cleaned_data['fecha_creacion']
        medio_ingreso = form.cleaned_data['medio_ingreso']
        tipo_solicitud = form.cleaned_data['tipo_solicitud']
        estado_expediente = form.cleaned_data['estado_expediente']
        grupo_etario = form.cleaned_data['grupo_etario']
        edad_persona = form.cleaned_data['edad_persona']
        situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        resumen_intervencion = form.cleaned_data['resumen_intervencion']
        tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        expediente_fisico = form.cleaned_data['expediente_fisico']
        clave_sisfe = form.cleaned_data['clave_sisfe']
        cuij = form.cleaned_data['cuij']
        observaciones = form.cleaned_data['observaciones']
        
        
        expediente = Expediente.objects.create(
            fecha_de_juzgado=fecha_de_juzgado,
            fecha_de_recepcion=fecha_de_recepcion,
            sede=sede,
            fecha_creacion=fecha_creacion,
            medio_ingreso=medio_ingreso,
            tipo_solicitud = tipo_solicitud,
            estado_expediente = estado_expediente,
            grupo_etario = grupo_etario,
            edad_persona = edad_persona,
            situacion_habitacional_hist = situacion_habitacional_hist,
            resumen_intervencion = resumen_intervencion,
            tipo_patrocinio = tipo_patrocinio,
            expediente_fisico = expediente_fisico,
            clave_sisfe = clave_sisfe,
            cuij = cuij,
            observaciones = observaciones,

        )
        for documento_form in documento_formset:
            if documento_form.cleaned_data.get('archivo'):
                documento = documento_form.save(commit=False)
                documento.expediente = expediente
                documento.save()

        messages.success(self.request, "El expediente fue creado correctamente.")
        return super().form_valid(form)
        

    def form_invalid(self, form):
        # Muestra mensaje si hubo errores
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error en {field.label}: {error}")
        messages.error(self.request, "Hubo errores al guardar el expediente. Verifique los campos.")
        return super().form_invalid(form)



class SecretariaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'expediente/secretaria_form.html'
    form_class = SecretariaForm
    success_url = reverse_lazy('expediente:expediente_list')
    login_url = 'core:login'
    permission_required = 'expediente.change_expediente'
    raise_exception = False

    def get_object(self):
        # Obtiene el expediente por la pk de la URL
        return get_object_or_404(Expediente, pk=self.kwargs['pk'])

    def get_initial(self):
        # Carga los datos existentes del expediente en el formulario
        expediente = self.get_object()
        initial = super().get_initial()

        initial.update({
            'fecha_de_juzgado': expediente.fecha_de_juzgado,
            'fecha_de_recepcion': expediente.fecha_de_recepcion,
            'sede': expediente.sede,
            'fecha_creacion': expediente.fecha_creacion,
            'medio_ingreso': expediente.medio_ingreso,
            'tipo_solicitud': expediente.tipo_solicitud,
            'estado_expediente': expediente.estado_expediente,
            'grupo_etario': expediente.grupo_etario,
            'edad_persona': expediente.edad_persona,
            'situacion_habitacional_hist': expediente.situacion_habitacional_hist,
            'resumen_intervencion': expediente.resumen_intervencion,
            'tipo_patrocinio': expediente.tipo_patrocinio,
            'expediente_fisico': expediente.expediente_fisico,
            'clave_sisfe': expediente.clave_sisfe,
            'cuij': expediente.cuij,
            'observaciones': expediente.observaciones,
        })
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        expediente = self.get_object()  # obtenemos el expediente que se está editando

        form = form_class(
            user=self.request.user,
            expediente=expediente,  # 👈 pasamos la instancia al form
            **self.get_form_kwargs()
        )

        form.fields['medio_ingreso'].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.get_object()

        if self.request.POST:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                self.request.POST, 
                self.request.FILES, 
                queryset=expediente.documentos.all()
            )
        else:
            context['documento_formset'] = ExpedienteDocumentoFormSet(
                queryset=expediente.documentos.all()
            )

        # Indicar que es edición
        context['editar'] = True

        # Número de expediente
        context['numero_expediente'] = expediente.identificador  # ajustar según tu campo real

        return context

    def form_valid(self, form):
        # Actualiza el expediente con los nuevos datos
        expediente = self.get_object()
        context = self.get_context_data()
        #documento_formset = context['documento_formset']

        #if not documento_formset.is_valid():
        #    messages.error(self.request, "Hay errores en los documentos. Corrígelos antes de continuar.")
        #    return self.form_invalid(form)

        expediente.fecha_de_juzgado = form.cleaned_data['fecha_de_juzgado']
        expediente.fecha_de_recepcion = form.cleaned_data['fecha_de_recepcion']
        expediente.sede = form.cleaned_data['sede']
        expediente.fecha_creacion = form.cleaned_data['fecha_creacion']
        expediente.medio_ingreso = form.cleaned_data['medio_ingreso']
        expediente.tipo_solicitud = form.cleaned_data['tipo_solicitud']
        expediente.estado_expediente = form.cleaned_data['estado_expediente']
        expediente.grupo_etario = form.cleaned_data['grupo_etario']
        expediente.edad_persona = form.cleaned_data['edad_persona']
        expediente.situacion_habitacional_hist = form.cleaned_data['situacion_habitacional_hist']
        expediente.resumen_intervencion = form.cleaned_data['resumen_intervencion']
        expediente.tipo_patrocinio = form.cleaned_data.get('tipo_patrocinio')
        expediente.expediente_fisico = form.cleaned_data['expediente_fisico']
        expediente.clave_sisfe = form.cleaned_data['clave_sisfe']
        expediente.cuij = form.cleaned_data['cuij']
        expediente.observaciones = form.cleaned_data['observaciones']
        expediente.save()

        # Actualiza o crea los documentos asociados
        #for documento_form in documento_formset:
        #    if documento_form.cleaned_data.get('archivo'):
        #        documento = documento_form.save(commit=False)
        #        documento.expediente = expediente
        #        documento.save()

        messages.success(self.request, "El expediente fue actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Muestra mensaje si hubo errores, incluyendo los de cada campo
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error en {field.label}: {error}")
        messages.error(self.request, "Hubo errores al actualizar el expediente. Verifique los campos.")
        return super().form_invalid(form)        



class SecretariaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Expediente
    template_name = "expediente/secretaria_detalle.html"
    context_object_name = "expediente"
    login_url = 'core:login'
    permission_required = 'expediente.view_expediente'
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Documentos asociados al expediente
        context["documentos"] = ExpedienteDocumento.objects.filter(expediente=self.object)
        return context


    
class ExpedienteDocumentoCreateView(FormView):
    template_name = 'expediente/documento_form.html'
    form_class = ExpedienteDocumentoForm

    def dispatch(self, request, *args, **kwargs):
        self.expediente = get_object_or_404(Expediente, pk=kwargs['expediente_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        documento = form.save(commit=False)
        documento.expediente = self.expediente
        documento.save()
        messages.success(self.request, "Documento agregado correctamente.")
        return redirect('expediente:expediente_detail', pk=self.expediente.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expediente'] = self.expediente
        return context



class ExpedienteDocumentoDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        documento = get_object_or_404(ExpedienteDocumento, pk=pk)
        expediente_id = documento.expediente.pk
        documento.delete()
        messages.success(request, "Documento eliminado correctamente.")
        return redirect("expediente:expediente_detail", pk=expediente_id)
    

# Vista basada en función para subir documentos de un expediente
@login_required(login_url = 'core:login')
@permission_required('expediente.add_expedientedocumento', login_url='core:login', raise_exception=True)
def expediente_documentos_view(request, expediente_id):
    # Obtiene el expediente por ID
    expediente = get_object_or_404(Expediente, id=expediente_id)

    if request.method == "POST":
        # Si el usuario envió archivos, procesa el formset
        formset = ExpedienteDocumentoFormSet(request.POST, request.FILES, queryset=ExpedienteDocumento.objects.none())
        if formset.is_valid():
            # Guarda cada documento subido
            for form in formset:
                if form.cleaned_data.get('archivo'):  # si realmente cargaron un archivo
                    documento = form.save(commit=False)
                    documento.expediente = expediente
                    documento.save()
            messages.success(request, "Documentos cargados correctamente.")
            return redirect("expediente:expediente_detail", pk=expediente.id)
    else:
        # Si es GET, muestra el formulario vacío
        formset = ExpedienteDocumentoFormSet(queryset=ExpedienteDocumento.objects.none())

    # Renderiza el formulario HTML con los documentos y expediente
    return render(request, "expediente/expediente_documentos_form.html", {
        "formset": formset,
        "expediente": expediente,
    })
    

@login_required(login_url='core:login')
@permission_required('expediente.view_expediente', login_url='core:login', raise_exception=True)
def expediente_list(request):
    user = request.user  # Obtenemos el usuario logueado
    next_url = request.GET.get("next")  # Capturamos 'next' si viene por parámetro

    # Si el usuario tiene una sede asociada, filtramos por ella
    if hasattr(user, "sede") and user.sede:
        expedientes = Expediente.objects.filter(sede=user.sede).order_by('-identificador')
    else:
        # Si el usuario no tiene sede, no mostramos nada
        expedientes = Expediente.objects.none()

    # Renderizamos el template con el contexto
    return render(request, "expediente/expediente_buscar.html", {
        "expedientes": expedientes,
        "next_url": next_url,
    })



class ExpedienteDocumentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExpedienteDocumento
    success_url = reverse_lazy('expediente:expediente_detail')
    login_url = 'core:login'
    permission_required = 'expediente.delete_expedientedocumento'
    raise_exception = False

    def post(self, request, pk, *args, **kwargs):
        documento = get_object_or_404(ExpedienteDocumento, pk=pk)
        expediente_id = documento.expediente.pk
        documento.delete()
        messages.success(request, "Documento eliminado correctamente.")
        return redirect("expediente:expediente_detail", pk=expediente_id)
    

# This class defines a view for creating instances of ExpedienteInstitucion with additional context
# data related to an Expediente object.
class ExpedienteInstitucionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExpedienteInstitucion
    form_class = ExpedienteInstitucionForm
    success_url = reverse_lazy('expediente:expediente_institucion_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expedienteinstitucion'
    raise_exception = False
    template_name = 'expediente/expediente_institucion_form.html'

    def get_initial(self):
        initial = super().get_initial()
        expediente_id = self.request.GET.get('expediente')
        if expediente_id:
            initial['expediente'] = expediente_id
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente_id = self.request.GET.get('expediente')
        numero_expediente = None
        if expediente_id:
            try:
                expediente = Expediente.objects.get(id=expediente_id)
                numero_expediente = expediente.identificador
            except Expediente.DoesNotExist:
                numero_expediente = None
        context['numero_expediente'] = numero_expediente
        context['instituciones'] = Institucion.objects.all()
        context['roles'] = Rol.objects.all()
        return context



class ExpedienteInstitucionCreateByIdView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExpedienteInstitucion
    form_class = ExpedienteInstitucionForm
    success_url = reverse_lazy('expediente:expediente_institucion_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expedienteinstitucion'
    raise_exception = False
    template_name = 'expediente/expediente_institucion_form_by_id.html'

    def get_initial(self):
        initial = super().get_initial()
        expediente_id = self.kwargs.get('expediente_id')
        institucion_id = self.request.GET.get('institucion_id')

        if expediente_id:
            initial['expediente'] = expediente_id
        
        if institucion_id:
            initial['institucion'] = institucion_id

        return initial


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente_id = self.kwargs.get('expediente_id')
        numero_expediente = None
        if expediente_id:
            try:
                expediente = Expediente.objects.get(id=expediente_id)
                numero_expediente = expediente.identificador
            except Expediente.DoesNotExist:
                numero_expediente = None
        context['numero_expediente'] = numero_expediente
        context['expediente_id'] = expediente_id
        context['instituciones'] = Institucion.objects.all()
        context['roles'] = Rol.objects.all()

        institucion_id = self.request.GET.get('institucion_id')  # o como estés recibiéndolo
        if institucion_id:
            try:
                context['institucion_seleccionada'] = Institucion.objects.get(id=institucion_id)
            except Institucion.DoesNotExist:
                context['institucion_seleccionada'] = None
        
        return context

    def form_valid(self, form):
        print("POST recibido:", self.request.POST)  # útil si querés ver si el ID llega

        accion = self.request.POST.get('accion')
        response = super().form_valid(form)

        if accion == "guardar":
            messages.success(self.request, "Se ha agregado Institución y Rol al expediente correctamente.")
            return redirect('expediente:expediente_institucion_list')

        if accion == "internacion":
            messages.success(self.request, "Se ha agregado Institución y Rol al expediente correctamente.")
            return redirect(
                reverse(
                    'internacion:internacion_create',
                    kwargs={'expediente_institucion_id': self.object.id}
                )
            )

        messages.success(self.request, "Se ha agregado Institución y Rol al expediente correctamente.")
        return redirect('expediente:expediente_institucion_list')




class ExpedientePersonaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExpedientePersona
    form_class = ExpedientePersonaForm
    success_url = reverse_lazy('expediente:expediente_persona_list')
    login_url = 'core:login'
    permission_required = 'expediente.add_expedientepersona'
    raise_exception = False
    template_name = 'expediente/expediente_persona_form.html'

    def get_initial(self):
        initial = super().get_initial()
        expediente_id = self.request.GET.get('expediente')
        if expediente_id:
            initial['expediente'] = expediente_id
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente_id = self.request.GET.get('expediente')
        numero_expediente = None
        if expediente_id:
            try:
                expediente = Expediente.objects.get(id=expediente_id)
                numero_expediente = expediente.identificador
            except Expediente.DoesNotExist:
                numero_expediente = None
        context['numero_expediente'] = numero_expediente
        context['personas'] = Persona.objects.all()
        context['roles'] = Rol.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "✅ El expediente se guardó correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "⚠️ No se pudo guardar el expediente. La persona ya tiene ese rol asociado.")
        return super().form_invalid(form)



# 🔹 Esta vista muestra un listado de registros del modelo ExpedienteInstitucion
class ExpedienteInstitucionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    # Modelo base de la vista
    model = ExpedienteInstitucion

    # Template HTML donde se mostrará la lista
    template_name = 'expediente/expediente_institucion_list.html'

    # Nombre que se usará en el template para acceder a la lista de objetos
    context_object_name = 'expediente_instituciones'

    # Permiso requerido para acceder a esta vista
    permission_required = 'expediente.view_expedienteinstitucion'

    # Si el usuario no tiene permiso, no lanza excepción 403 (podés poner True si querés)
    raise_exception = False


    # ✅ Sobrescribimos el método get_queryset()
    # Este método define qué objetos del modelo se van a mostrar
    def get_queryset(self):
        # Obtenemos el usuario que está logueado
        user = self.request.user

        # Verificamos que el usuario esté autenticado y tenga una sede asociada
        if user.is_authenticated and hasattr(user, 'sede'):
            # Filtramos los expedientes para mostrar solo los de la sede del usuario
            # Además, usamos select_related() para optimizar las consultas a las FK
            return (
                ExpedienteInstitucion.objects
                .filter(expediente__sede=user.sede)   # 👈 filtra por sede
                .select_related('expediente', 'institucion', 'rol')  # 👈 mejora eficiencia
            )
        else:
            # Si el usuario no tiene sede (o no está logueado), no mostramos ningún registro
            return ExpedienteInstitucion.objects.none()


    # ✅ Agregamos datos adicionales al contexto del template
    def get_context_data(self, **kwargs):
        # Obtenemos el contexto base de la clase padre
        context = super().get_context_data(**kwargs)

        # Agregamos el usuario actual al contexto (por si querés usarlo en el template)
        context['user'] = self.request.user

        # Retornamos el contexto completo al template
        return context



class ExpedientePersonaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExpedientePersona
    template_name = 'expediente/expediente_persona_list.html'
    context_object_name = 'expediente_personas'
    permission_required = 'expediente.view_expedientepersona'
    raise_exception = False  # Lanza 403 si no tiene permiso

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'sede'):
            return ExpedientePersona.objects.filter(expediente__sede=user.sede).select_related('expediente', 'persona', 'rol')
        else:
            return ExpedientePersona.objects.none()  # Si no hay usuario o sede, no mostrar nada

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


@login_required(login_url='core:login')
@permission_required('expediente.add_expedienteinstitucion', login_url='core:login', raise_exception=True)
def expediente_institucion_add_view(request):
    if request.method == "POST":
        # Procesar y guardar los datos aquí
        form = ExpedienteInstitucionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La institución fue vinculada correctamente al expediente.")
            return redirect('expediente:expediente_institucion_list')
        
    context = {
        "expedientes": Expediente.objects.all(),
        "instituciones": Institucion.objects.filter(estado=True),
        "roles": Rol.objects.all(),
    }
    return render(request, "expediente/expediente_institucion_form.html", context)


@login_required(login_url='core:login')
@permission_required('expediente.add_expedientepersona', login_url='core:login', raise_exception=True)
def buscar_instituciones(request):
    q = request.GET.get('q', '')
    instituciones = Institucion.objects.filter(institucion__icontains=q)[:20]
    results = [{'id': i.id, 'text': i.institucion} for i in instituciones]
    return JsonResponse({'results': results})


@login_required(login_url='core:login')
@permission_required('expediente.add_expedientepersona', login_url='core:login', raise_exception=True)
def buscar_personas(request):
    q = request.GET.get('q', '')
    personas = Persona.objects.filter(
        Q(nombre__icontains=q) | Q(apellido__icontains=q)
    )[:20]
    results = [{'id': i.id, 'text': f"{i.nombre} {i.apellido}"} for i in personas]
    return JsonResponse({'results': results})


def handler403(request, exception=None):
    return render(request, '403.html', status=403)

def buscar_expediente(request):
    query = request.GET.get('q', '')
    expedientes = Expediente.objects.filter(
        Q(cuij__icontains=query) | Q(clave_sisfe__icontains=query)
    )
    return render(request, 'expediente/expediente_buscar.html', {
        'expedientes': expedientes,
        'query': query,
    })


###########################################
####Estadisticas de Expedientes############
###########################################

class EstadisticasRangoFechasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'expediente/rango_fechas.html'
    context_object_name = 'expedientes'
    permission_required = 'expediente.view_expediente'
    raise_exception = False  # Lanza 403 si no tiene permiso

    def get_queryset(self):
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        return Expediente.objects.fecha_rango(fecha_inicio, fecha_fin)
      