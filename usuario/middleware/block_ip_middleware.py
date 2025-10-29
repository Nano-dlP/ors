# usuario/middleware/block_ip_middleware.py
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

def _get_client_ip(request):
    """Obtiene la IP real del cliente, incluso detrás de proxies."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        ip = xff.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "unknown"


class BlockIPMiddleware:
    """
    Middleware que revisa si la IP o el usuario están bloqueados.
    Permite excluir IPs en lista blanca o desactivar completamente el bloqueo.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.block_prefix_ip = "blocked:ip:"
        self.block_prefix_user = "blocked:user:"

    def __call__(self, request):
        # 🔹 Si el sistema de bloqueo está deshabilitado, continuar normal
        if not getattr(settings, "IP_BLOCK_ATTEMPT_LIMIT", 5):
            return self.get_response(request)

        ip = _get_client_ip(request)

        # 🔹 Si la IP está en lista blanca, continuar sin verificar
        whitelist = getattr(settings, "IP_WHITELIST", [])
        if ip in whitelist:
            return self.get_response(request)

        # 🔹 Bloqueo por IP
        if cache.get(self.block_prefix_ip + ip):
            return render(
                request,
                "usuario/ip_bloqueada.html",
                {"mensaje": "Tu IP está temporalmente bloqueada."},
                status=403,
            )

        # 🔹 Bloqueo por usuario (opcional, si se envía username/email)
        if request.method == "POST" and request.path.startswith("/login"):
            username = request.POST.get("username") or request.POST.get("email")
            if username and cache.get(self.block_prefix_user + username.lower()):
                return render(
                    request,
                    "usuario/usuario_bloqueado.html",
                    {"mensaje": "Este usuario está temporalmente bloqueado."},
                    status=403,
                )

        # 🔹 Si todo bien, continuar
        response = self.get_response(request)
        return response