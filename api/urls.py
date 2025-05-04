from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExpenseViewSet, CategoryViewSet, IncomeViewSet, GoalViewSet,
    predict_category, generate_report, generate_forecast,
    expense_statistics, expenses_by_category, monthly_expenses,
    category_summary, income_statistics, goal_progress
)

router = DefaultRouter()
router.register('expenses', ExpenseViewSet, basename='expense')
router.register('categories', CategoryViewSet, basename='category')
router.register('incomes', IncomeViewSet, basename='income')
router.register('goals', GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
    path('expenses/stats/', expense_statistics, name='expense-stats'),
    path('expenses/by-category/', expenses_by_category, name='expenses-by-category'),
    path('expenses/monthly/', monthly_expenses, name='monthly-expenses'),
    path('categories/summary/', category_summary, name='category-summary'),
    path('incomes/stats/', income_statistics, name='income-stats'),
    path('goals/progress/', goal_progress, name='goal-progress'),
    path('reports/generate/', generate_report, name='generate-report'),
    path('analytics/forecast/', generate_forecast, name='generate-forecast'),
    path('ml/predict-category/', predict_category, name='predict-category'),
]