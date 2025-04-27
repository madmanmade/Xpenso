from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from .models import Report

@receiver(post_save, sender=Report)
def handle_report_generation(sender, instance, created, **kwargs):
    """
    Handle report generation and caching when a new report is created or updated
    """
    if created:
        # Clear any cached reports for this user
        cache_key = f"user_reports_{instance.user.id}"
        cache.delete(cache_key)
        
        # You might want to trigger async report generation here
        # For now, we'll just pass as it's a placeholder
        pass

@receiver(post_delete, sender=Report)
def cleanup_report_files(sender, instance, **kwargs):
    """
    Clean up report files when a report is deleted
    """
    # Clear cache
    cache_key = f"user_reports_{instance.user.id}"
    cache.delete(cache_key)
    
    # Clean up stored report file if it exists
    if instance.file:
        try:
            instance.file.delete(save=False)
        except Exception:
            # Log the error but don't raise it
            pass 