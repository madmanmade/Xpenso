from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Expense(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('other', 'Other')
    )
    
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.amount}"

    class Meta:
        ordering = ['-date', '-created_at']
        
    def get_category_name(self):
        """Returns the category name or 'Uncategorized' if no category"""
        return self.category.name if self.category else 'Uncategorized'
    
    def to_dict(self):
        """Convert expense to dictionary format for API responses"""
        return {
            'id': self.id,
            'amount': float(self.amount),
            'description': self.description,
            'category': self.get_category_name(),
            'payment_method': self.get_payment_method_display(),
            'date': self.date.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'owner': self.owner.username
        }

class Budget(models.Model):
    PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.get_period_display()})"

    def is_active(self):
        today = timezone.now().date()
        if self.end_date:
            return self.start_date <= today <= self.end_date
        return self.start_date <= today

    def get_spent_amount(self):
        expenses = Expense.objects.filter(
            owner=self.owner,
            category=self.category,
            date__gte=self.start_date
        )
        if self.end_date:
            expenses = expenses.filter(date__lte=self.end_date)
        return expenses.aggregate(total=models.Sum('amount'))['total'] or 0

    def get_remaining_amount(self):
        spent = self.get_spent_amount()
        return self.amount - spent

    def get_progress_percentage(self):
        spent = self.get_spent_amount()
        return (spent / self.amount) * 100 if self.amount > 0 else 0