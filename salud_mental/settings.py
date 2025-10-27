"""
Django settings for salud_mental project.

Notas de cambios:
- Se añadió import os (se estaba usando más abajo sin importar).
- Lectura de secrets_casa.json envuelta para no romper si el archivo no existe.
- get_secret ahora busca en el dict de secrets y como fallback en variables de entorno.
- Revisa y provee SECRET_KEY y demás claves sensibles en producción.
"""

from django.core.exceptions import ImproperlyConfigured
import json
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar secrets desde un archivo JSON (opcional) sin romper si no existe.
secrets_path = BASE_DIR / 'secrets_casa.json'
if secrets_path.exists():
    try:
        with open(secrets_path, 'r', encoding='utf-8') as f:
            secrets = json.load(f)
    except Exception as e:
        # Si el archivo existe pero falla la lectura, lanzamos excepción clara
        raise ImproperlyConfigured(f"Error leyendo {secrets_path}: {e}")
else:
    # Si no existe el archivo, usamos un dict vacío y permitimos fallback a env vars
    secrets = {}

def get_secret(setting, secrets=secrets):
    """
    Obtiene la clave del diccionario `secrets` o, si no está, la busca en las
    variables de entorno. Si no existe en ninguno, lanza ImproperlyConfigured.

    Esto permite ejecutar comandos de mantenimiento (collectstatic, etc.) si
    se definen variables de entorno en vez del archivo secrets_json.
    """
    # 1) intentar desde el archivo secrets (si existe)
    if setting in secrets:
        return secrets[setting]
    # 2) fallback a variable de entorno
    env_val = os.environ.get(setting)
    if env_val is not None:
        return env_val
    # 3) no existe: error explícito
    raise ImproperlyConfigured(f"Set the {setting} environment variable or include it in {secrets_path}")

# SECURITY WARNING: keep the secret key used in production secret!
# Secret obligatorio: si falta lanzamos excepción para forzar su provisión.
SECRET_KEY = get_secret('SECRET_KEY')

# DEBUG: conviene configurar vía variable de entorno en producción
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')

# Allowed hosts: puede venir de secrets o env var (ej: "example.com,api.example.com")
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]
else:
    # Intenta leer desde secrets si existe la clave
    try:
        ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS').split(',') if get_secret('ALLOWED_HOSTS') else []
    except ImproperlyConfigured:
        ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',  # Para ajustar renderizado de formularios en templates

    # Apps de la aplicación (ajusta/añade según tu proyecto)
    'core',
    'persona',
    'usuario',
    'institucion',
    'expediente',
    'internacion',
    'intervencion',
    'profesional',
]

# Cache: LocMem en desarrollo, Redis en producción (mejor rendimiento/compartido)
if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-dev-cache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get("REDIS_LOCATION", "redis://127.0.0.1:6379/1"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manejo de sesiones
    'usuario.middleware.block_ip_middleware.BlockIPMiddleware',  # Bloqueo por IP (si usas)
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',  # Timeout de sesión

    # Middleware personalizado (se puede desactivar si impacta performance)
    'core.middleware.RegistrarClienteMiddleware',
]

# Configuración de expirado de sesión (usa django-session-timeout)
SESSION_EXPIRE_SECONDS = int(os.environ.get('SESSION_EXPIRE_SECONDS', 60))  # segundos
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = int(os.environ.get('SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD', 60))
SESSION_TIMEOUT_REDIRECT = 'core:login'

SESSION_COOKIE_AGE = int(os.environ.get('SESSION_COOKIE_AGE', 3600))  # 1 hora por defecto
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Parámetros bloqueo por IP (valores por defecto; puedes sobreescribir con env vars)
IP_BLOCK_ATTEMPT_LIMIT = int(os.environ.get('IP_BLOCK_ATTEMPT_LIMIT', 3))
IP_BLOCK_ATTEMPT_WINDOW = int(os.environ.get('IP_BLOCK_ATTEMPT_WINDOW', 5 * 60))
IP_BLOCK_TIME = int(os.environ.get('IP_BLOCK_TIME', 60 * 15))

ROOT_URLCONF = 'salud_mental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.fecha_hora_actual',
            ],
        },
    },
]

WSGI_APPLICATION = 'salud_mental.wsgi.application'

# Database: se esperan valores en secrets o variables de entorno.
# Nota: Django acepta strings para PORT, pero puedes castear a int si prefieres.
DATABASES = {
    "default": {
        "ENGINE": get_secret('ENGINE'),
        "NAME": get_secret('NAME'),
        "USER": get_secret('USER'),
        "PASSWORD": get_secret('PASSWORD'),
        "HOST": get_secret('HOST'),
        "PORT": get_secret('PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'es'
USE_I18N = True
# NOTE: USE_L10N was deprecated in recent Django versions; si tu versión lo requiere, mantenlo.
USE_L10N = True
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'usuario.CustomUser'

# Configuración del correo electrónico
# En desarrollo: console backend para evitar envíos reales
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # En producción: esperamos que las claves estén en secrets o en variables de entorno.
    # get_secret ya hace fallback a env vars, por eso aquí no envolvemos en try/except.
    EMAIL_BACKEND = get_secret('EMAIL_BACKEND')
    EMAIL_HOST = get_secret('EMAIL_HOST')
    # Convertir puerto a int cuando sea aplicable
    EMAIL_PORT = int(get_secret('EMAIL_PORT')) if get_secret('EMAIL_PORT') else None
    # Normalizar booleanos comunes para EMAIL_USE_TLS
    raw_use_tls = get_secret('EMAIL_USE_TLS')
    if isinstance(raw_use_tls, bool):
        EMAIL_USE_TLS = raw_use_tls
    else:
        EMAIL_USE_TLS = str(raw_use_tls).lower() in ('1', 'true', 'yes')
    EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
    EMAIL_FILE_PATH = get_secret('EMAIL_FILE_PATH')

# Mensajes (Bootstrap mapping)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}