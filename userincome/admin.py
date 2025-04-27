from django.contrib import admin

# Register your models here.
from .models import UserIncome, Source

class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'source', 'date')
    search_fields = ('description', 'source', 'date')
    list_per_page = 10

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(UserIncome, UserIncomeAdmin)
admin.site.register(Source, SourceAdmin)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'source', 'date')
    list_filter = ('source', 'date')
    ordering = ('-date',)
    search_fields = ('description', 'source__name', 'owner__username')
    list_per_page = 20

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
