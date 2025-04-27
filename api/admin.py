from django.contrib import admin

# Register your models here.
from .models import Expense, Category

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date', 'user')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
