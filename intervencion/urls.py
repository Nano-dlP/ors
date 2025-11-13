from django.urls import path

from .views import listar_intervenciones, IntevencionListView, IntervencionCreateView
from . import views

app_name = 'intervencion'

urlpatterns = [
    path('intervencion/', IntervencionCreateView.as_view(), name='intervencion_create'),
    path('intervenciones/', listar_intervenciones, name='intervencion_list'),
    path('intervencion/listar/', IntevencionListView.as_view(), name='intervencion_list'),
       
]
