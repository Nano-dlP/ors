# usuario/apps.py
from django.apps import AppConfig

class UsuarioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuario"

    def ready(self):
        # Al importar signals se registra el handler
        import usuario.signals  # noqa
