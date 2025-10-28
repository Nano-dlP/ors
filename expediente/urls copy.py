from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (DemandaEspontaneaCreateView, 
                    ExpedienteListView, 
                    MedioIngresoSelectView, 
                    OficioCreateView, 
                    SecretariaCreateView, 
                    DemandaEspontaneaUpdateView, 
                    ExpedienteUpdateDispatcherView, 
                    OficioUpdateView, 
                    SecretariaUpdateView, 
                    expediente_list, 
                    ExpedienteDocumentoCreateView,
                    DemandaEspontaneaDetailView,
                    ExpedienteDocumentoDeleteView,
                    ExpedienteDetailDispatcherView, 
                    OficioDetailView,
                    SecretariaDetailView,
                    ExpedienteInstitucionCreateView,
                    ExpedienteInstitucionListView,
                    ExpedientePersonaListView,
                    expediente_institucion_add_view,
                    ExpedientePersonaCreateView,
                    buscar_instituciones,
                    buscar_personas
        )

from . import views

app_name = 'expediente'

urlpatterns = [
    # Listar expedientes
    path('expediente/', ExpedienteListView.as_view(), name='expediente_list'),
    
    # Crear expediente - seleccionar medio de ingreso
    path('expediente/seleccionar-medio/', MedioIngresoSelectView.as_view(), name='medio_ingreso_select'),
    
    # Crear expediente - Es demanda espontanea, osea está la persona o se tiene datos de la misma
    path('expediente/crear/<int:medio_id>/', DemandaEspontaneaCreateView.as_view(), name='expediente_create_with_medio'),
    
    # Crear expediente - Es por intermedio de un oficio Judicial o administrativo (Instituciones, etc)
    path('expediente/crear_oficio/<int:medio_id>/', OficioCreateView.as_view(), name='expediente_create_oficio'),
    
    # Crear expediente - Es por intermedio de un oficio (defensoría)
    path('expediente/crear_oficio_sec/<int:medio_id>/', SecretariaCreateView.as_view(), name='expediente_create'),
    
    # Editar expedientes
    path('expediente/demanda_editar/<int:pk>/', DemandaEspontaneaUpdateView.as_view(), name='demanda_espontanea_update'),
    path('expediente/oficio_editar/<int:pk>/', OficioUpdateView.as_view(), name='oficio_update'),
    path('expediente/secretaria_editar/<int:pk>/', SecretariaUpdateView.as_view(), name='secretaria_update'),

    # Redirigir a la vista de edición y detalle correspondiente según el tipo de expediente
    path('expediente/editar/<int:pk>/', ExpedienteUpdateDispatcherView.as_view(), name='expediente_update'),
    path('expediente/detalle/<int:pk>/', ExpedienteDetailDispatcherView.as_view(), name='expediente_detail'),

    # Buscar expedientes
    path('expediente/buscar/', expediente_list, name='expediente_buscar'),
    
    # Agregar y eliminar documentos asociados a un expediente
    path('expediente/<int:expediente_id>/agregar-documento/', ExpedienteDocumentoCreateView.as_view(), name='expediente_agregar_documento'),
    path('documento/<int:pk>/eliminar/', ExpedienteDocumentoDeleteView.as_view(), name='expediente_documento_delete'),

    # Detalle específico para expedientes por demanda espontánea
    path('demanda-espontanea/<int:pk>/', DemandaEspontaneaDetailView.as_view(), name='demanda_espontanea_detail'),
    # Detalle específico para expedientes por oficio
    path('oficio/<int:pk>/detalle/', OficioDetailView.as_view(), name='oficio_detail'),
    # Detalle específico para expedientes por secretaria
    path('secretaria/<int:pk>/detalle/', SecretariaDetailView.as_view(), name='secretaria_detail'),

    path ('expediente/crear_institucion/', ExpedienteInstitucionCreateView.as_view(), name='expediente_institucion_create'),
    path ('expediente/institucion/', ExpedienteInstitucionListView.as_view(), name='expediente_institucion_list'),

    path('expediente/persona/agregar/', ExpedientePersonaCreateView.as_view(), name='expediente_persona_create'),
    path('expediente/persona/', ExpedientePersonaListView.as_view(), name='expediente_persona_list'),
    
    path('api/instituciones/', buscar_instituciones, name='buscar_instituciones'),
    path('api/personas/', buscar_personas, name='buscar_personas'),

]
