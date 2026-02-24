from django.urls import path
from . import views

app_name = 'internacion'

urlpatterns = [
    path('internacion/listar/', views.InternacionListView.as_view(), name='internacion_list'),
    path('internacion/crear/<int:expediente_institucion_id>/', views.InternacionCreateView.as_view(), name='internacion_create'),

    path('internacion/editar/<int:pk>/', views.InternacionUpdateView.as_view(), name='internacion_edit'),
    path('internacion/detalle/<int:pk>/', views.InternacionDetailView.as_view(), name='internacion_detail'),
    path('internacion/motivo-internacion/', views.InternacionMotivoInternacion.as_view(), name='internacion_motivo_internacion'),
    path('internacion/motivo-alta/', views.InternacionMotivoAlta.as_view(), name='internacion_motivo_alta'),
]