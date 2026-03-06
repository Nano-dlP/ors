from django.urls import path

from .views import listar_intervenciones, IntevencionListView, IntervencionCreateView, IntervencionDetailView, IntervencionUpdateView
from . import views

app_name = 'intervencion'

urlpatterns = [
    path('intervencion/', IntervencionCreateView.as_view(), name='intervencion_create'),
    #path('intervenciones/', listar_intervenciones, name='intervencion_list'),
    path('intervencion/listar/', IntevencionListView.as_view(), name='intervencion_list'),
    path('intervencion/detalle<int:pk>/', IntervencionDetailView.as_view(), name='intervencion_detail'),
    path('intervencion/editar/<int:pk>/', IntervencionUpdateView.as_view(), name='intervencion_update'),
       
]
