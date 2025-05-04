from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """Extended user profile model with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_avatars/', null=True, blank=True)
    currency_preference = models.CharField(max_length=3, default='USD')
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notification_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    budget_alerts = models.BooleanField(default=True)
    goal_reminders = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class UserPreference(models.Model):
    """User preferences for app customization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    weekly_report = models.BooleanField(default=True)
    monthly_report = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"

    class Meta:
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'
