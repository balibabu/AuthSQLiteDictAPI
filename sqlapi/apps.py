from django.apps import AppConfig


class SqlapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sqlapi'


    def ready(self):
        import sqlapi.signals