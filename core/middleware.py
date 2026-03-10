from django.conf import settings
from .utils import registrar_cliente

class RegistrarClienteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Apagar/encender registro desde settings
        if not getattr(settings, "CLIENTELOG_ENABLED", True):
            return response

        # Solo registrar si no es admin o static/media
        if (
            not request.path.startswith('/admin')
            and not request.path.startswith('/static')
            and not request.path.startswith('/media')
        ):
            try:
                registrar_cliente(request)
            except Exception:
                pass

        return response