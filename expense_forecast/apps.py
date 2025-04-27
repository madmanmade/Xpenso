from django.apps import AppConfig


class ExpenseForecastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expense_forecast'
    verbose_name = 'Expense Forecast'

    def ready(self):
        """Initialize app configurations and signals"""
        # Import signals to register them
        from . import signals
