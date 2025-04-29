from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Expense(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

    class Meta:
        ordering = ['-date']
        permissions = [
            ("can_view_expenses", "Can view expenses"),
            ("can_add_expenses", "Can add expenses"),
            ("can_edit_expenses", "Can edit expenses"),
            ("can_delete_expenses", "Can delete expenses"),
        ]
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['category']),
        ]
