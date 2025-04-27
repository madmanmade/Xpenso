from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, default='USD')
    theme = models.CharField(max_length=20, default='light')
    notification_enabled = models.BooleanField(default=True)
    budget_alert_threshold = models.IntegerField(default=80)  # Percentage
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    expense_categories = models.JSONField(default=dict)  # Store custom expense categories
    income_categories = models.JSONField(default=dict)  # Store custom income categories
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    email_notifications = models.BooleanField(default=True)
    mobile_notifications = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'
    
    def __str__(self):
        return f"{self.user.username}'s preferences"
        
    def get_formatted_currency(self):
        """Returns the currency in proper format for display"""
        return self.currency.upper()
        
    def toggle_notification(self, notification_type):
        """Toggle notification settings"""
        if notification_type == 'email':
            self.email_notifications = not self.email_notifications
        elif notification_type == 'mobile':
            self.mobile_notifications = not self.mobile_notifications
        self.save()
