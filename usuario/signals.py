# usuario/signals.py
from django.contrib.auth.signals import user_login_failed
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Configurables en settings.py (usa los tuyos si ya existen)
ATTEMPT_LIMIT = getattr(settings, "IP_BLOCK_ATTEMPT_LIMIT", 3)
ATTEMPT_WINDOW = getattr(settings, "IP_BLOCK_ATTEMPT_WINDOW", 5 * 60)  # segundos
BLOCK_TIME = getattr(settings, "IP_BLOCK_TIME", 60 * 60)  # segundos

def _get_client_ip(request):
    # Cuidado con X-Forwarded-For — solo usar si estás detrás de proxy de confianza
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        ip = xff.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "unknown"

def _cache_key_ip(ip):
    return f"login_attempts:ip:{ip}"

def _cache_key_user(username):
    return f"login_attempts:user:{username.lower()}"

def _cache_key_block_ip(ip):
    return f"blocked:ip:{ip}"

def _cache_key_block_user(username):
    return f"blocked:user:{username.lower()}"

def login_failed(sender, credentials, request, **kwargs):
    """
    Signal handler para user_login_failed.
    Incrementa contador de intentos para IP y para username; bloquea si supera el límite.
    """
    try:
        ip = _get_client_ip(request) if request is not None else "unknown"
    except Exception:
        ip = "unknown"

    username = credentials.get("username") or credentials.get("email") or "unknown"

    # --- IP attempts ---
    ip_key = _cache_key_ip(ip)
    ip_count = cache.get(ip_key, 0) + 1
    cache.set(ip_key, ip_count, timeout=ATTEMPT_WINDOW)
    logger.debug("Failed login attempt IP=%s count=%s", ip, ip_count)

    if ip_count >= ATTEMPT_LIMIT:
        cache.set(_cache_key_block_ip(ip), True, timeout=BLOCK_TIME)
        logger.warning("IP blocked: %s for %s seconds", ip, BLOCK_TIME)

    # --- User attempts ---
    user_key = _cache_key_user(username)
    user_count = cache.get(user_key, 0) + 1
    cache.set(user_key, user_count, timeout=ATTEMPT_WINDOW)
    logger.debug("Failed login attempt USER=%s count=%s", username, user_count)

    if user_count >= ATTEMPT_LIMIT:
        cache.set(_cache_key_block_user(username), True, timeout=BLOCK_TIME)
        logger.warning("User blocked: %s for %s seconds", username, BLOCK_TIME)

# conectar la señal (se importará desde apps.py)
user_login_failed.connect(login_failed)
