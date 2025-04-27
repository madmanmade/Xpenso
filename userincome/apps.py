from django.apps import AppConfig


class UserincomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userincome'
    verbose_name = 'User Income'
    
    def ready(self):
        import userincome.signals
        # Register signals for income tracking
        from django.db.models.signals import post_save, post_delete
        from django.dispatch import receiver
        from .models import UserIncome
        
        # Set up signal handlers for income analytics
        @receiver(post_save, sender=UserIncome)
        def update_income_stats(sender, instance, created, **kwargs):
            if created:
                # Update user's total income and other relevant metrics
                pass
                
        @receiver(post_delete, sender=UserIncome) 
        def remove_income_stats(sender, instance, **kwargs):
            # Recalculate stats when income deleted
            pass
