path('crear/<int:expediente_institucion_id>/', views.InternacionCreateView.as_view(), name='internacion_create'),
path('editar/<int:pk>/', views.InternacionUpdateView.as_view(), name='internacion_update'),
