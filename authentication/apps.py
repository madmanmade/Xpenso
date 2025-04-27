from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    def ready(self):
        """
        Initialize app configurations and signals when the app is ready.
        This method is called once when Django starts.
        """
        # Import signals to register them
        import authentication.signals
