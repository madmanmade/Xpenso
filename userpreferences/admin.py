from django.contrib import admin

# Register your models here.
from .models import UserPreference

admin.site.register(UserPreference)
