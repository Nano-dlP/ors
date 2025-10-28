"""
Django settings for salud_mental project.

Notas de cambios:
- Se reemplaza la carga desde secrets_casa.json por .env usando python-dotenv.
- Se añade helper get_env para leer/castear y validar variables de entorno.
- SECRET_KEY es obligatorio y lanzará ImproperlyConfigured si falta.
- DEBUG por defecto False (más seguro); se puede activar vía .env en desarrollo.
- ALLOWED_HOSTS se lee desde ALLOWED_HOSTS (comas) en .env; en producción no puede quedar vacío.
- Ajustes de EMAIL, DATABASES y CACHES ahora usan variables de entorno.
"""

from django.core.exceptions import ImproperlyConfigured
import os
from pathlib import Path

# Opcional: python-dotenv (instalar con pip install python-dotenv)
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar .env si python-dotenv está disponible y existe el archivo
DOTENV_PATH = BASE_DIR / '.env'
if load_dotenv:
    # load_dotenv acepta Path objects en versiones recientes
    load_dotenv(dotenv_path=DOTENV_PATH, override=False)

def get_env(name, default=None, required=False, cast=None):
    """
    Lee una variable de entorno, permite casting y valida presencia si required=True.
    - name: nombre de la variable de entorno.
    - default: valor por defecto si no existe.
    - required: si True, lanza ImproperlyConfigured cuando no existe o está vacío.
    - cast: función para convertir el string (ej. int, lambda x: x.lower() in (...))
    """
    val = os.environ.get(name, default)
    if required and (val is None or str(val) == ''):
        raise ImproperlyConfigured(f"Falta la variable de entorno {name}. Añadila en {DOTENV_PATH} o configúrala en el entorno.")
    if cast is not None and val is not None and val != '':
        try:
            return cast(val)
        except Exception as e:
            raise ImproperlyConfigured(f"Error casteando la variable {name}: {e}")
    return val

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env('SECRET_KEY', required=True)

# DEBUG: por seguridad usar False por defecto. Activar con DEBUG=1|true|yes en .env localmente.
DEBUG = get_env('DEBUG', default='False', cast=lambda v: str(v).strip().lower() in ('1', 'true', 'yes'))

# Allowed hosts: ALLOWED_HOSTS="example.com,api.example.com"
_allowed_hosts_env = get_env('ALLOWED_HOSTS', default='')
if _allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in str(_allowed_hosts_env).split(',') if h.strip()]
else:
    ALLOWED_HOSTS = []

# En producción no permitimos ALLOWED_HOSTS vacío
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS no puede estar vacío en modo producción. Define ALLOWED_HOSTS en el .env o en el entorno.")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',

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
            "LOCATION": get_env("REDIS_LOCATION", default="redis://127.0.0.1:6379/1"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'usuario.middleware.block_ip_middleware.BlockIPMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'core.middleware.RegistrarClienteMiddleware',
]

# Configuración de expirado de sesión (usa django-session-timeout)
SESSION_EXPIRE_SECONDS = int(get_env('SESSION_EXPIRE_SECONDS', default=60))
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = int(get_env('SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD', default=60))
SESSION_TIMEOUT_REDIRECT = 'core:login'

SESSION_COOKIE_AGE = int(get_env('SESSION_COOKIE_AGE', default=3600))
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

IP_BLOCK_ATTEMPT_LIMIT = int(get_env('IP_BLOCK_ATTEMPT_LIMIT', default=3))
IP_BLOCK_ATTEMPT_WINDOW = int(get_env('IP_BLOCK_ATTEMPT_WINDOW', default=5 * 60))
IP_BLOCK_TIME = int(get_env('IP_BLOCK_TIME', default=60 * 15))

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

# Database: se esperan valores en variables de entorno (.env)
DATABASES = {
    "default": {
        "ENGINE": get_env('DB_ENGINE', required=True),
        "NAME": get_env('DB_NAME', required=True),
        "USER": get_env('DB_USER', required=True),
        "PASSWORD": get_env('DB_PASSWORD', required=True),
        "HOST": get_env('DB_HOST', required=True),
        "PORT": get_env('DB_PORT', default=''),
    }
}
# Si DB_PORT viene vacía, Django acepta cadena vacía; si prefieres int, castealo:
if DATABASES["default"]["PORT"]:
    try:
        DATABASES["default"]["PORT"] = int(DATABASES["default"]["PORT"])
    except ValueError:
        # dejar como string si no es convertible
        pass

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
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = get_env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
    DEFAULT_FROM_EMAIL = 'webmaster@localhost'
    EMAIL_HOST = get_env('EMAIL_HOST', required=True)
    EMAIL_PORT = get_env('EMAIL_PORT', default='')
    if EMAIL_PORT:
        try:
            EMAIL_PORT = int(EMAIL_PORT)
        except ValueError:
            raise ImproperlyConfigured("EMAIL_PORT debe ser un entero.")
    raw_use_tls = get_env('EMAIL_USE_TLS', default='False')
    EMAIL_USE_TLS = str(raw_use_tls).strip().lower() in ('1', 'true', 'yes')
    EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', default='')
    EMAIL_FILE_PATH = get_env('EMAIL_FILE_PATH', default=None)

# Mensajes (Bootstrap mapping)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
