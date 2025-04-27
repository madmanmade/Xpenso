from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'expense_forecast/index.html')

@login_required(login_url='/authentication/login')
def generate_forecast(request):
    if request.method == 'POST':
        # Add forecast generation logic here
        forecast_data = {
            'forecast': [],
            'confidence_interval': []
        }
        return JsonResponse(forecast_data)
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
