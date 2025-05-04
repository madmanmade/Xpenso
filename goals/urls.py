from django.urls import path
from . import views

urlpatterns = [
    # Goal management URLs
    path('', views.index, name='goals'),
    path('add/', views.add_goal, name='add_goal'),
    path('edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('delete/<int:id>/', views.delete_goal, name='delete_goal'),
    path('goal/<int:id>/', views.goal_details, name='goal_details'),
    path('goal/<int:id>/update/', views.update_goal_progress, name='update_goal_progress'),
    
    # Savings goals URLs
    path('savings/', views.savings_goals_list, name='savings_goals_list'),
    path('savings/add/', views.add_savings_goal, name='add_savings_goal'),
    path('savings/<int:goal_id>/edit/', views.edit_savings_goal, name='edit_savings_goal'),
    path('savings/<int:goal_id>/delete/', views.delete_savings_goal, name='delete_savings_goal'),
    path('savings/<int:goal_id>/update-amount/', views.update_savings_amount, name='update_savings_amount'),
]