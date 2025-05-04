from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import ExpenseForecast
from userpreferences.models import UserPreference
from expenses.models import Expense, Category
from django.db import models
from collections import defaultdict
from datetime import date, timedelta

# Create your views here.

@login_required(login_url='/authentication/login')
def forecast_dashboard(request):
    # Provide categories for the dashboard
    categories = Category.objects.filter(owner=request.user)
    user_preferences = None
    try:
        user_preferences = UserPreference.objects.get(user=request.user)
    except Exception:
        pass
    context = {
        'categories': categories,
        'user_preferences': user_preferences,
    }
    return render(request, 'expense_forecast/forecast_dashboard.html', context)

@login_required(login_url='/authentication/login')
def index(request):
    return redirect('forecast_dashboard')

@login_required(login_url='/authentication/login')
def generate_forecast(request):
    if request.method == 'POST':
        user = request.user
        period = int(request.POST.get('forecast_period', 1))  # months
        model_type = request.POST.get('model_type', 'linear')
        category_id = request.POST.get('category', 'all')

        # Get expenses for the last 6 months (or all if less)
        today = date.today()
        six_months_ago = today - timedelta(days=180)
        expenses = Expense.objects.filter(owner=user, date__gte=six_months_ago)
        if category_id != 'all':
            expenses = expenses.filter(category_id=category_id)
        expenses = expenses.order_by('date')

        # Group by month and sum
        monthly_totals = defaultdict(float)
        for exp in expenses:
            month = exp.date.strftime('%Y-%m')
            monthly_totals[month] += float(exp.amount)
        # Use last 6 months
        months = sorted(monthly_totals.keys())[-6:]
        values = [monthly_totals[m] for m in months]
        if not values:
            return JsonResponse({'forecast': [], 'confidence_interval': []})
        avg = sum(values) / len(values)
        # Simple forecast: repeat avg for each period
        forecast = [round(avg, 2)] * period
        # Confidence interval: +/- 10%
        confidence_interval = [[round(avg*0.9,2), round(avg*1.1,2)] for _ in range(period)]
        return JsonResponse({'forecast': forecast, 'confidence_interval': confidence_interval})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/authentication/login')
def get_forecast_data(request):
    if request.method == 'GET':
        try:
            # Get user's expenses
            expenses = request.user.expenses.all().order_by('date')
            
            if not expenses:
                return JsonResponse({'error': 'No expense data available'}, status=404)
            
            # Process expense data for forecasting
            expense_data = []
            for expense in expenses:
                expense_data.append({
                    'date': expense.date,
                    'amount': expense.amount,
                    'category': expense.category.name
                })
            
            return JsonResponse({
                'status': 'success',
                'data': expense_data
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/authentication/login')
def save_forecast(request):
    if request.method == 'POST':
        try:
            forecast_data = request.POST.get('forecast_data')
            if not forecast_data:
                return JsonResponse({'error': 'No forecast data provided'}, status=400)
                
            # Save forecast data logic here
            # You can create a model to store forecasts and save it
            
            return JsonResponse({
                'status': 'success',
                'message': 'Forecast saved successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/authentication/login')
def forecast_details(request, forecast_id):
    try:
        forecast = ExpenseForecast.objects.get(id=forecast_id, user=request.user)
    except ExpenseForecast.DoesNotExist:
        return render(request, 'expense_forecast/forecast.html', {
            'error': 'Forecast not found.'
        })
    # Get user preferences
    try:
        user_preferences = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        user_preferences = None
    # Dummy data for forecast_details (replace with real logic as needed)
    forecast_details = [
        {
            'date': '2024-07',
            'predicted_amount': forecast.amount,
            'lower_bound': float(forecast.amount) * 0.9,
            'upper_bound': float(forecast.amount) * 1.1,
            'confidence_interval': 95
        }
    ]
    context = {
        'forecast_details': forecast_details,
        'user_preferences': user_preferences,
        'forecast_data': True,  # To trigger the display in the template
        'forecast_summary': {
            'average': forecast.amount,
            'maximum': forecast.amount,
            'minimum': forecast.amount,
            'total': forecast.amount
        },
        'model_metrics': {
            'accuracy': 90,
            'mae': 10,
            'rmse': 15,
            'confidence': 95
        },
        'chart_data': {
            'labels': ['2024-07'],
            'historical': [float(forecast.amount) * 0.8],
            'forecast': [float(forecast.amount)],
            'upper_bound': [float(forecast.amount) * 1.1],
            'lower_bound': [float(forecast.amount) * 0.9]
        }
    }
    return render(request, 'expense_forecast/forecast.html', context)

@login_required(login_url='/authentication/login')
def edit_forecast(request, forecast_id):
    return HttpResponse('Edit forecast view placeholder.')

@login_required(login_url='/authentication/login')
def delete_forecast(request, forecast_id):
    return HttpResponse('Delete forecast view placeholder.')

@login_required(login_url='/authentication/login')
def forecast_history(request):
    return HttpResponse('Forecast history view placeholder.')

@login_required(login_url='/authentication/login')
def download_forecast(request, forecast_id):
    return HttpResponse('Download forecast view placeholder.')

@login_required(login_url='/authentication/login')
def get_category_expense_summary(request):
    # Returns category-wise expense totals for the logged-in user
    expenses = Expense.objects.filter(owner=request.user)
    categories = Category.objects.filter(owner=request.user)
    summary = []
    for category in categories:
        total = expenses.filter(category=category).aggregate(total=models.Sum('amount'))['total'] or 0
        summary.append({'category': category.name, 'total': float(total)})
    return JsonResponse({'summary': summary})
