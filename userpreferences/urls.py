from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='preferences'),
    path('update/', views.update_preferences, name='update_preferences'), 
    path('toggle-notification/', views.toggle_notification, name='toggle_notification'),
    path('update-theme/', views.update_theme, name='update_theme'),
    path('update-language/', views.update_language, name='update_language'),
    path('update-timezone/', views.update_timezone, name='update_timezone'),
    path('update-budget/', views.update_budget, name='update_budget'),
    path('update-savings-goal/', views.update_savings_goal, name='update_savings_goal'),
    path('update-categories/', views.update_categories, name='update_categories'),
    path('update-notification-settings/', views.update_notification_settings, name='update_notification_settings'),
    path('update-budget-alert/', views.update_budget_alert, name='update_budget_alert'),
    path('export-preferences/', views.export_preferences, name='export_preferences'),
    path('import-preferences/', views.import_preferences, name='import_preferences'),
]