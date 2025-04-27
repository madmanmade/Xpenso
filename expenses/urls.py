from django.urls import path
from . import views
from . import ml_models

urlpatterns = [
    # Core expense management
    path('', views.index, name='expenses'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:id>/', views.expense_edit, name='expense_edit'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    
    # Category management
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('category-summary/', views.expense_category_summary, name='expense_category_summary'),
    
    # ML and prediction
    path('predict-category/', views.predict_category, name='predict_category'),
    path('train-model/', views.train_expense_model, name='train_expense_model'),
    
    # Data and analytics
    path('search/', views.search_expenses, name='search_expenses'),
    path('export/', views.export_expenses, name='export_expenses'),
    path('stats/', views.expense_statistics, name='expense_statistics'),
    
    # Additional analytics
    path('monthly-summary/', views.monthly_summary, name='monthly_summary'),
    path('yearly-summary/', views.yearly_summary, name='yearly_summary'),
    path('payment-method-summary/', views.payment_method_summary, name='payment_method_summary'),
    
    # Budget management
    path('budget/', views.manage_budget, name='manage_budget'),
    path('budget/add/', views.add_budget, name='add_budget'),
    path('budget/edit/<int:id>/', views.edit_budget, name='edit_budget'),
    path('budget/delete/<int:id>/', views.delete_budget, name='delete_budget'),
    
    # Reports
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/download/<str:report_id>/', views.download_report, name='download_report'),
]