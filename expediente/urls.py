from django.urls import path, re_path
from .views import (
    DemandaEspontaneaCreateView, 
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
    ExpedientePersonaCreateView,
    expediente_institucion_add_view,
    buscar_instituciones,
    buscar_personas
)

app_name = 'expediente'

urlpatterns = [
    # Rutas existentes
    path('expediente/', ExpedienteListView.as_view(), name='expediente_list'),
    path('expediente/seleccionar-medio/', MedioIngresoSelectView.as_view(), name='medio_ingreso_select'),
    path('expediente/crear/<int:medio_id>/', DemandaEspontaneaCreateView.as_view(), name='expediente_create_with_medio'),
    path('expediente/crear_oficio/<int:medio_id>/', OficioCreateView.as_view(), name='expediente_create_oficio'),
    path('expediente/crear_oficio_sec/<int:medio_id>/', SecretariaCreateView.as_view(), name='expediente_create'),
    path('expediente/demanda_editar/<int:pk>/', DemandaEspontaneaUpdateView.as_view(), name='demanda_espontanea_update'),
    path('expediente/oficio_editar/<int:pk>/', OficioUpdateView.as_view(), name='oficio_update'),
    path('expediente/secretaria_editar/<int:pk>/', SecretariaUpdateView.as_view(), name='secretaria_update'),
    path('expediente/editar/<int:pk>/', ExpedienteUpdateDispatcherView.as_view(), name='expediente_update'),
    path('expediente/detalle/<int:pk>/', ExpedienteDetailDispatcherView.as_view(), name='expediente_detail'),
    path('expediente/buscar/', expediente_list, name='expediente_buscar'),
    path('expediente/<int:expediente_id>/agregar-documento/', ExpedienteDocumentoCreateView.as_view(), name='expediente_agregar_documento'),
    path('documento/<int:pk>/eliminar/', ExpedienteDocumentoDeleteView.as_view(), name='expediente_documento_delete'),
    path('demanda-espontanea/<int:pk>/', DemandaEspontaneaDetailView.as_view(), name='demanda_espontanea_detail'),
    path('oficio/<int:pk>/detalle/', OficioDetailView.as_view(), name='oficio_detail'),
    path('secretaria/<int:pk>/detalle/', SecretariaDetailView.as_view(), name='secretaria_detail'),
    path('expediente/crear_institucion/', ExpedienteInstitucionCreateView.as_view(), name='expediente_institucion_create'),
    path('expediente/institucion/', ExpedienteInstitucionListView.as_view(), name='expediente_institucion_list'),
    path('expediente/persona/agregar/', ExpedientePersonaCreateView.as_view(), name='expediente_persona_create'),
    path('expediente/persona/', ExpedientePersonaListView.as_view(), name='expediente_persona_list'),
    path('api/instituciones/', buscar_instituciones, name='buscar_instituciones'),
    path('api/personas/', buscar_personas, name='buscar_personas'),

    # ------------------------------
    # Catch-all para ignorar cualquier texto extra
    # Debe ir al final para no interferir con las rutas específicas
    re_path(r'^expediente/.*$', ExpedienteListView.as_view()),
    re_path(r'^expediente/persona/.*$', ExpedientePersonaListView.as_view()),
]
