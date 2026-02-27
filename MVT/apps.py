from django.apps import AppConfig


class MvtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MVT'

def ready(self):
        import MVT.signals  # ensures signals are loaded