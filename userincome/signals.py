from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserIncome
from django.db import models

@receiver(post_save, sender=UserIncome)
def update_income_stats(sender, instance, created, **kwargs):
    """
    Update income statistics when a new income is added or updated
    """
    if created:
        # Update user's total income
        user = instance.user
        total_income = UserIncome.objects.filter(user=user).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        # You can store this in a UserProfile or similar model
        # For now, we'll just pass as it's a placeholder
        pass

@receiver(post_delete, sender=UserIncome)
def remove_income_stats(sender, instance, **kwargs):
    """
    Recalculate income statistics when an income is deleted
    """
    user = instance.user
    total_income = UserIncome.objects.filter(user=user).aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    # You can store this in a UserProfile or similar model
    # For now, we'll just pass as it's a placeholder
    pass 