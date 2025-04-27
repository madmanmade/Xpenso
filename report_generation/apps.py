from django.apps import AppConfig


class ReportGenerationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'report_generation'
    verbose_name = 'Report Generation'

    def ready(self):
        """
        Import signals when app is ready
        """
        import report_generation.signals
        # Register any app configurations or initializations here
        from django.conf import settings
        
        # Initialize report generation settings if needed
        if hasattr(settings, 'REPORT_GENERATION_SETTINGS'):
            self.report_settings = settings.REPORT_GENERATION_SETTINGS
        else:
            self.report_settings = {
                'default_format': 'pdf',
                'storage_path': 'reports/',
                'enable_caching': True,
                'cache_timeout': 3600  # 1 hour
            }
