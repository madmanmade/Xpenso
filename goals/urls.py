from django.urls import path
from . import views

urlpatterns = [
    # Goal management URLs
    path('', views.index, name='goals'),
    path('add/', views.add_goal, name='add_goal'),
    path('edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('delete/<int:id>/', views.delete_goal, name='delete_goal'),
    
    # Goal progress tracking
    path('progress/<int:id>/', views.goal_progress, name='goal_progress'),
    path('progress/<int:id>/add/', views.add_progress, name='add_progress'),
    path('progress/<int:id>/history/', views.progress_history, name='progress_history'),
    
    # Goal reminder URLs
    path('reminder/<int:id>/', views.goal_reminder, name='goal_reminder'),
    path('reminder/<int:id>/add/', views.add_reminder, name='add_reminder'), 
    path('reminder/<int:id>/edit/', views.edit_reminder, name='edit_reminder'),
    path('reminder/<int:id>/delete/', views.delete_reminder, name='delete_reminder'),
    
    # Goal category management
    path('categories/', views.goal_categories, name='goal_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:id>/delete/', views.delete_category, name='delete_category'),
    
    # Goal analytics and reporting
    path('analytics/', views.goal_analytics, name='goal_analytics'),
    path('reports/', views.goal_reports, name='goal_reports'),
    path('reports/export/', views.export_goal_data, name='export_goal_data'),
]