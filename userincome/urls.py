from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='income'),
    path('add-income/', views.add_income, name='add-income'), 
    path('edit-income/<int:id>/', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>/', views.delete_income, name='delete-income'),
    path('search-income/', views.search_income, name='search-income'),
    path('income-source/', views.income_source, name='income-source'),
    path('add-source/', views.add_source, name='add-source'),
    path('edit-source/<int:id>/', views.edit_source, name='edit-source'), 
    path('delete-source/<int:id>/', views.delete_source, name='delete-source'),
    path('income-summary/', views.income_summary, name='income-summary'),
    path('income-stats/', views.income_stats, name='income-stats'),
    path('export-income/', views.export_income, name='export-income'),
    path('income-detail/<int:id>/', views.income_detail, name='income-detail'),
    path('income-category/', views.income_category, name='income-category'),
    path('add-category/', views.add_category, name='add-category'),
    path('edit-category/<int:id>/', views.edit_category, name='edit-category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete-category'),
    path('income-report/', views.income_report, name='income-report'),
    path('income-chart/', views.income_chart, name='income-chart'),
    path('income-pdf/', views.income_pdf, name='income-pdf'),
    path('income-csv/', views.income_csv, name='income-csv'),
]