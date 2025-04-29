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
    path('income-detail/<int:id>/', views.income_detail, name='income-detail'),
]