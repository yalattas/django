from django.apps import AppConfig


class PointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.points'

    def ready(self):
        from . import signals