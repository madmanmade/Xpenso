from django.db import models
from django.utils import timezone

class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ]
    
    REPORT_TYPES = [
        ('EXPENSE', 'Expense Report'),
        ('INCOME', 'Income Report'),
        ('BUDGET', 'Budget Report'),
        ('GOALS', 'Goals Report'),
        ('SUMMARY', 'Summary Report')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reports')
    data = models.JSONField(null=True, blank=True)  # Store report data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_report_type_display()}"

    class Meta:
        ordering = ['-created_at']

class ReportTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=Report.REPORT_TYPES)
    content = models.TextField()  # Template content/structure
    parameters = models.JSONField()  # Required parameters for the template
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"

    class Meta:
        ordering = ['name']
        verbose_name = 'Report Template'
        verbose_name_plural = 'Report Templates'
