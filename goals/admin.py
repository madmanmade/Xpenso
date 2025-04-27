from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FinancialGoal, GoalCategory, GoalProgress, GoalReminder

@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'current_amount', 'deadline', 'category', 'status')
    list_filter = ('status', 'category', 'deadline')
    search_fields = ('title', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(GoalProgress)
class GoalProgressAdmin(admin.ModelAdmin):
    list_display = ('goal', 'amount_added', 'date')
    list_filter = ('date', 'goal')
    search_fields = ('goal__title',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(goal__user=request.user)

@admin.register(GoalReminder)
class GoalReminderAdmin(admin.ModelAdmin):
    list_display = ('goal', 'reminder_date', 'is_active')
    list_filter = ('reminder_date', 'is_active')
    search_fields = ('goal__title',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(goal__user=request.user)
