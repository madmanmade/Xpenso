from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPreference

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Create UserPreference instance when a new user is created
    """
    if created:
        UserPreference.objects.get_or_create(user=instance) 