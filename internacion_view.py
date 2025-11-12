class InternacionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Internacion
    form_class = InternacionForm
    template_name = 'internacion/internacion_form.html'
    permission_required = 'internacion.add_internacion'
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente_institucion_id = self.kwargs.get('expediente_institucion_id')
        context['editar'] = False
        context['expediente_institucion'] = get_object_or_404(ExpedienteInstitucion, id=expediente_institucion_id)
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.expediente_institucion = get_object_or_404(
            ExpedienteInstitucion,
            id=self.kwargs.get('expediente_institucion_id')
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('internacion:internacion_list')


class InternacionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Internacion
    form_class = InternacionForm
    template_name = 'internacion/internacion_form.html'
    permission_required = 'internacion.change_internacion'
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editar'] = True
        context['expediente_institucion'] = self.object.expediente_institucion
        return context

    def get_success_url(self):
        return reverse_lazy('internacion:internacion_list')
