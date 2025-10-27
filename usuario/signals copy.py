from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.core.cache import cache
from .blocked_ip_helpers import add_blocked_ip, BLOCKED_KEY_PREFIX

MAX_FAILED_ATTEMPTS = 3
BLOCK_TIME = 300  # 5 minutos

@receiver(user_login_failed)
def bloquea_ip_login_fallido(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    if not ip:
        return

    cache_key = f"failed_login:{ip}"
    failed_attempts = cache.get(cache_key, 0) + 1
    cache.set(cache_key, failed_attempts, timeout=BLOCK_TIME)

    if failed_attempts >= MAX_FAILED_ATTEMPTS:
        add_blocked_ip(ip, block_time=BLOCK_TIME)
        # Opcional: resetear contador de intentos tras bloqueo
        cache.delete(cache_key)


def get_client_ip(request):
    """Detecta la IP real del cliente, incluso detrás de proxy."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
