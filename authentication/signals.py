from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, UserPreference

@receiver(post_save, sender=User)
def create_user_profile_and_preferences(sender, instance, created, **kwargs):
    """
    Create UserProfile and UserPreference when a new user is created
    """
    if created:
        # Create UserProfile
        UserProfile.objects.create(user=instance)
        
        # Create UserPreference
        UserPreference.objects.create(user=instance)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Send a welcome email when a new user is created
    """
    if created:
        # This is just a placeholder. Email sending should be configured in settings.py
        try:
            send_mail(
                'Welcome to Xpenso!',
                f'Hi {instance.username},\n\nWelcome to Xpenso! We are excited to have you on board.',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=True,
            )
        except Exception:
            # Log the error but don't raise it
            pass 