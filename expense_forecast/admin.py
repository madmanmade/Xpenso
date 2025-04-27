from django.contrib import admin

# Register your models here.
from .models import ExpenseForecast, ForecastCategory

@admin.register(ExpenseForecast)
class ExpenseForecastAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'forecast_date', 'created_at')
    list_filter = ('category', 'forecast_date', 'created_at')
    search_fields = ('user__username', 'category__name')
    date_hierarchy = 'forecast_date'
    ordering = ('-forecast_date',)

@admin.register(ForecastCategory) 
class ForecastCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
