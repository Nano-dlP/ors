from auditoria.signals import set_current_user

class AuditoriaUsuarioMiddleware:
    """Guarda el usuario actual en una variable local accesible por signals."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            set_current_user(request.user)
        response = self.get_response(request)
        return response
