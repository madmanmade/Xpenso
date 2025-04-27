from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from .models import ExpenseForecast

@receiver(post_save, sender=ExpenseForecast)
def update_forecast_analytics(sender, instance, created, **kwargs):
    """
    Update analytics when a new forecast is created or updated
    """
    if created:
        # Calculate total forecasted expenses for the user
        user_forecasts = ExpenseForecast.objects.filter(user=instance.user)
        total_forecast = user_forecasts.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        # You can store this in a UserProfile or similar model
        # For now, we'll just pass as it's a placeholder
        pass

@receiver(post_delete, sender=ExpenseForecast)
def recalculate_forecast_analytics(sender, instance, **kwargs):
    """
    Recalculate analytics when a forecast is deleted
    """
    # Recalculate total forecasted expenses for the user
    user_forecasts = ExpenseForecast.objects.filter(user=instance.user)
    total_forecast = user_forecasts.aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    # You can store this in a UserProfile or similar model
    # For now, we'll just pass as it's a placeholder
    pass 