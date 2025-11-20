from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (InstitucionCreateView, 
                    InstitucionListView, 
                    InstitucionUpdateView, 
                    InstitucionDetailView, 
                    desactivar_institucion, 
                    listar_institucion,
                    listar_institucion_by_id,
                     )

from . import views

app_name = 'institucion'

urlpatterns = [
    path('institucion/', InstitucionListView.as_view(), name='institucion_list'),
    path('institucion/nuevo/', InstitucionCreateView.as_view(), name='institucion_create'),
    path('institucion/editar/<int:pk>/', InstitucionUpdateView.as_view(), name='institucion_edit'),
    path('institucion/detalle/<int:pk>/', InstitucionDetailView.as_view(), name='institucion_detail'),
    path('institucion/desactivar/<int:pk>', desactivar_institucion, name="institucion_deactivate"),
    
    path('institucion/agregar_expediente/', listar_institucion, name='agregar_expediente'),
    path('institucion/agregar_expediente_by_id/', listar_institucion_by_id, name='agregar_expediente_by_id'),
]
