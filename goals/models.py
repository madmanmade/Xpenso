from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings

class GoalCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Goal Categories"

class FinancialGoal(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    current_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    deadline = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_goals')
    category = models.ForeignKey(GoalCategory, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def progress(self):
        return (self.current_amount / self.target_amount) * 100 if self.target_amount > 0 else 0

    @property
    def days_remaining(self):
        return (self.deadline - timezone.now().date()).days

    def is_achievable(self):
        if self.days_remaining <= 0:
            return False
        required_daily_saving = (self.target_amount - self.current_amount) / self.days_remaining
        return required_daily_saving <= self.user.income.average_monthly_income / 30

class GoalProgress(models.Model):
    goal = models.ForeignKey(FinancialGoal, on_delete=models.CASCADE, related_name='progress_records')
    amount_added = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

class GoalReminder(models.Model):
    goal = models.ForeignKey(FinancialGoal, on_delete=models.CASCADE, related_name='reminders')
    reminder_date = models.DateField()
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['reminder_date']
        indexes = [
            models.Index(fields=['reminder_date', 'is_active']),
            models.Index(fields=['goal', 'reminder_date']),
        ]
    
    def __str__(self):
        return f"Reminder for {self.goal.title} on {self.reminder_date}"
        
    def is_due_soon(self):
        """Check if reminder is due within the next 7 days"""
        days_until_reminder = (self.reminder_date - timezone.now().date()).days
        return 0 <= days_until_reminder <= 7
    
    def mark_as_inactive(self):
        """Mark reminder as inactive"""
        self.is_active = False
        self.save()
        
    def reschedule(self, new_date):
        """Reschedule reminder to a new date"""
        if new_date <= timezone.now().date():
            raise ValueError("Reminder date must be in the future")
        self.reminder_date = new_date
        self.save()
