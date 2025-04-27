from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Source(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class UserIncome(models.Model):
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    description = models.TextField(blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    receipt = models.FileField(upload_to='income_receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.name} - ${self.amount}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Income'
        verbose_name_plural = 'Income'
        permissions = [
            ("can_view_all_income", "Can view all user income entries"),
            ("can_edit_all_income", "Can edit all user income entries"),
            ("can_delete_all_income", "Can delete all user income entries"),
            ("can_export_income", "Can export income data"),
            ("can_generate_income_reports", "Can generate income reports"),
        ]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['owner']),
            models.Index(fields=['source']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='income_amount_positive'
            )
        ]
