from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import FinancialGoal, GoalProgress, GoalReminder

@receiver(post_save, sender=FinancialGoal)
def create_goal_reminders(sender, instance, created, **kwargs):
    """
    Create reminders for a new financial goal
    """
    if created:
        # Create reminders based on configured thresholds
        from django.conf import settings
        
        for days in getattr(settings, 'GOAL_REMINDER_THRESHOLDS', [7, 3, 1]):
            reminder_date = instance.deadline - timezone.timedelta(days=days)
            if reminder_date > timezone.now().date():
                GoalReminder.objects.create(
                    goal=instance,
                    reminder_date=reminder_date,
                    message=f"Your goal '{instance.title}' deadline is in {days} days!"
                )

@receiver(post_save, sender=GoalProgress)
def update_goal_progress(sender, instance, created, **kwargs):
    """
    Update goal progress when a new progress record is added
    """
    if created:
        goal = instance.goal
        # Update current amount
        total_progress = GoalProgress.objects.filter(goal=goal).aggregate(
            total=models.Sum('amount_added')
        )['total'] or 0
        goal.current_amount = total_progress
        
        # Check if goal is completed
        if goal.current_amount >= goal.target_amount:
            goal.status = 'COMPLETED'
        
        goal.save()

@receiver(post_delete, sender=GoalProgress)
def recalculate_goal_progress(sender, instance, **kwargs):
    """
    Recalculate goal progress when a progress record is deleted
    """
    goal = instance.goal
    # Recalculate current amount
    total_progress = GoalProgress.objects.filter(goal=goal).aggregate(
        total=models.Sum('amount_added')
    )['total'] or 0
    goal.current_amount = total_progress
    goal.save() 