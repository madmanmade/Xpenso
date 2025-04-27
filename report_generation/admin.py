from django.contrib import admin

# Register your models here.
from .models import Report, ReportTemplate

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'report_type', 'status')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('title', 'user__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user')
        }),
        ('Report Details', {
            'fields': ('report_type', 'status', 'data')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'is_active', 'created_at')
    list_filter = ('report_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'description', 'report_type', 'is_active')
        }),
        ('Template Content', {
            'fields': ('content', 'parameters')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
