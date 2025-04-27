from django.apps import AppConfig


class GoalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goals'
    verbose_name = 'Financial Goals'
    
    def ready(self):
        """
        Initialize app configurations and register signals
        """
        import goals.signals  # Import signals
        
        # Initialize any required settings
        from django.conf import settings
        
        # Set default goal reminder thresholds if not configured
        if not hasattr(settings, 'GOAL_REMINDER_THRESHOLDS'):
            settings.GOAL_REMINDER_THRESHOLDS = [7, 3, 1]  # Days before deadline
            
        # Set default goal progress notification threshold
        if not hasattr(settings, 'GOAL_PROGRESS_NOTIFICATION_THRESHOLD'):
            settings.GOAL_PROGRESS_NOTIFICATION_THRESHOLD = 25  # Percentage milestones
            # Set default goal categories if not configured
            if not hasattr(settings, 'DEFAULT_GOAL_CATEGORIES'):
                settings.DEFAULT_GOAL_CATEGORIES = [
                    'Emergency Fund',
                    'Retirement',
                    'Home Purchase',
                    'Education',
                    'Debt Repayment',
                    'Travel',
                    'Vehicle',
                    'Investment'
                ]
            
            # Set default minimum goal duration in days
            if not hasattr(settings, 'MIN_GOAL_DURATION_DAYS'):
                settings.MIN_GOAL_DURATION_DAYS = 30  # Minimum 30 days for a goal
                
            # Set default maximum goal duration in years
            if not hasattr(settings, 'MAX_GOAL_DURATION_YEARS'): 
                settings.MAX_GOAL_DURATION_YEARS = 30  # Maximum 30 years for long-term goals
                
            # Set default goal progress calculation frequency in days
            if not hasattr(settings, 'GOAL_PROGRESS_CALCULATION_FREQUENCY'):
                settings.GOAL_PROGRESS_CALCULATION_FREQUENCY = 1  # Calculate progress daily
