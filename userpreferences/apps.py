from django.apps import AppConfig


class UserpreferencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userpreferences'
    verbose_name = 'User Preferences'

    def ready(self):
        """
        Import signals when the app is ready
        """
        import userpreferences.signals
