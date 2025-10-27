# usuario/middleware/block_ip_middleware.py
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        ip = xff.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "unknown"

class BlockIPMiddleware:
    """
    Middleware: revisa si la IP o el username (si provisto) está bloqueado.
    Si bloqueado, devuelve 403 o renderiza una página.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.block_prefix_ip = "blocked:ip:"
        self.block_prefix_user = "blocked:user:"

    def __call__(self, request):
        ip = _get_client_ip(request)

        if cache.get(self.block_prefix_ip + ip):
            # Renderizamos template personalizado y enviamos status 403
            return render(
                request,
                "usuario/ip_bloqueada.html",  # tu template
                {"mensaje": "Tu IP está temporalmente bloqueada."},
                status=403
            )

        # Opcional: bloque por usuario
        if request.method == "POST" and request.path.startswith("/login"):
            username = request.POST.get("username") or request.POST.get("email")
            if username and cache.get(self.block_prefix_user + username.lower()):
                return render(
                    request,
                    "usuario/usuario_bloqueado.html",
                    {"mensaje": "Este usuario está temporalmente bloqueado."},
                    status=403
                )

        response = self.get_response(request)
        return response