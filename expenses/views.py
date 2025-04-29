from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.core.exceptions import PermissionDenied
from .models import Expense, Category, Budget
from .forms import ExpenseForm, CategoryForm, BudgetForm
from .ml_models import ExpenseCategoryPredictor, train_and_save_model
import os
import csv
from django.conf import settings
from datetime import datetime, timedelta
import json
from decimal import Decimal
from django.db import models

@login_required(login_url='/authentication/login/')
def index(request):
    try:
        expenses = Expense.objects.filter(owner=request.user).order_by('-date')
        paginator = Paginator(expenses, settings.EXPENSE_PAGINATION_SIZE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
        context = {
            'expenses': page_obj,
            'total_expenses': total_expenses,
            'categories': Category.objects.filter(owner=request.user)
        }
        return render(request, 'expenses/index.html', context)
    except Exception as e:
        messages.error(request, f'Error loading expenses: {str(e)}')
        return redirect('/')

@login_required(login_url='authentication:login')
def add_expense(request):
    try:
        if request.method == 'POST':
            form = ExpenseForm(request.POST, user=request.user)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.owner = request.user
                expense.save()
                messages.success(request, 'Expense saved successfully')
                return redirect('expenses')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = ExpenseForm(user=request.user)
        
        context = {
            'form': form,
            'categories': Category.objects.filter(owner=request.user)
        }
        return render(request, 'expenses/add_expense.html', context)
    except Exception as e:
        messages.error(request, f'Error adding expense: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def expense_edit(request, id):
    try:
        expense = get_object_or_404(Expense, pk=id, owner=request.user)
        
        if request.method == 'POST':
            form = ExpenseForm(request.POST, instance=expense, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Expense updated successfully')
                return redirect('expenses')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = ExpenseForm(instance=expense, user=request.user)
        
        context = {
            'expense': expense,
            'form': form,
            'categories': Category.objects.filter(owner=request.user)
        }
        return render(request, 'expenses/edit_expense.html', context)
    except PermissionDenied:
        messages.error(request, 'You do not have permission to edit this expense')
        return redirect('expenses')
    except Exception as e:
        messages.error(request, f'Error editing expense: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def delete_expense(request, id):
    try:
        expense = get_object_or_404(Expense, pk=id, owner=request.user)
        expense.delete()
        messages.success(request, 'Expense deleted successfully')
    except PermissionDenied:
        messages.error(request, 'You do not have permission to delete this expense')
    except Exception as e:
        messages.error(request, f'Error deleting expense: {str(e)}')
    return redirect('expenses')

@login_required(login_url='authentication:login')
def expense_category_summary(request):
    expenses = Expense.objects.filter(owner=request.user)
    categories = Category.objects.filter(owner=request.user)
    
    summary = {}
    for category in categories:
        total = expenses.filter(category=category).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        if total['total']:
            summary[category.name] = {
                'amount': float(total['total']),
                'count': total['count']
            }
    
    return JsonResponse({'expense_category_data': summary})

@login_required(login_url='authentication:login')
def predict_category(request):
    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        if not description:
            return JsonResponse({
                'success': False,
                'error': 'Description is required'
            }, status=400)
        
        try:
            predictor = ExpenseCategoryPredictor()
            model_path = os.path.join(settings.BASE_DIR, 'expenses', 'trained_model.joblib')
            
            if os.path.exists(model_path):
                predictor.load_model(model_path)
            else:
                predictor = train_and_save_model()
            
            predictions = predictor.predict_proba(description)
            formatted_predictions = [
                {'category': cat, 'probability': float(prob)}
                for cat, prob in predictions
            ]
            
            return JsonResponse({
                'success': True,
                'predictions': formatted_predictions
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method',
        'message': 'This endpoint requires a POST request with a description field'
    }, status=405)

@login_required(login_url='authentication:login')
def train_expense_model(request):
    if request.method == 'POST':
        try:
            predictor = train_and_save_model()
            return JsonResponse({
                'success': True,
                'message': 'Model trained and saved successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required(login_url='authentication:login')
def search_expenses(request):
    try:
        if request.method == 'GET':
            query = request.GET.get('q', '').strip()
            if not query:
                return JsonResponse({
                    'success': False,
                    'error': 'Search query is required'
                }, status=400)
            
            expenses = Expense.objects.filter(
                owner=request.user,
                description__icontains=query
            ).order_by('-date')
            
            expenses_data = [{
                'id': expense.id,
                'amount': float(expense.amount),
                'description': expense.description,
                'category': expense.get_category_name(),
                'date': expense.date.strftime('%Y-%m-%d'),
                'payment_method': expense.get_payment_method_display()
            } for expense in expenses]
            
            return JsonResponse({
                'success': True,
                'expenses': expenses_data
            })
        
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        }, status=405)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required(login_url='authentication:login')
def export_expenses(request):
    try:
        expenses = Expense.objects.filter(owner=request.user).order_by('-date')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="expenses_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Category', 'Description', 'Amount', 'Payment Method'])
        
        for expense in expenses:
            writer.writerow([
                expense.date.strftime('%Y-%m-%d'),
                expense.get_category_name(),
                expense.description,
                expense.amount,
                expense.get_payment_method_display()
            ])
        
        return response
    except Exception as e:
        messages.error(request, f'Error exporting expenses: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def expense_statistics(request):
    try:
        expenses = Expense.objects.filter(owner=request.user)
        
        # Monthly trends
        monthly_expenses = expenses.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('month')
        
        # Category distribution
        category_expenses = expenses.values(
            'category__name'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Payment method distribution
        payment_method_expenses = expenses.values(
            'payment_method'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        context = {
            'monthly_expenses': list(monthly_expenses),
            'category_expenses': list(category_expenses),
            'payment_method_expenses': list(payment_method_expenses),
            'total_expenses': expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
            'avg_expense': expenses.aggregate(Avg('amount'))['amount__avg'] or 0
        }
        
        return render(request, 'expenses/statistics.html', context)
    except Exception as e:
        messages.error(request, f'Error loading statistics: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def monthly_summary(request):
    expenses = Expense.objects.filter(owner=request.user)
    
    # Get monthly summary for the last 12 months
    last_12_months = expenses.filter(
        date__gte=datetime.now() - timedelta(days=365)
    ).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount'),
        avg=Avg('amount'),
        count=Count('id')
    ).order_by('-month')
    
    return JsonResponse({
        'success': True,
        'monthly_summary': [{
            'month': item['month'].strftime('%Y-%m'),
            'total': float(item['total']),
            'average': float(item['avg']),
            'count': item['count']
        } for item in last_12_months]
    })

@login_required(login_url='authentication:login')
def yearly_summary(request):
    expenses = Expense.objects.filter(owner=request.user)
    
    # Get yearly totals
    yearly_data = expenses.annotate(
        year=models.functions.ExtractYear('date')
    ).values('year').annotate(
        total=Sum('amount'),
        avg=Avg('amount'),
        count=Count('id')
    ).order_by('-year')
    
    return JsonResponse({
        'success': True,
        'yearly_summary': list(yearly_data)
    })

@login_required(login_url='authentication:login')
def payment_method_summary(request):
    expenses = Expense.objects.filter(owner=request.user)
    
    # Get summary by payment method
    payment_summary = expenses.values(
        'payment_method'
    ).annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount')
    ).order_by('-total')
    
    return JsonResponse({
        'success': True,
        'payment_summary': [{
            'method': item['payment_method'],
            'total': float(item['total']),
            'average': float(item['avg']),
            'count': item['count']
        } for item in payment_summary]
    })

@login_required(login_url='authentication:login')
def manage_categories(request):
    try:
        categories = Category.objects.filter(owner=request.user)
        context = {
            'categories': categories,
            'form': CategoryForm()
        }
        return render(request, 'expenses/manage_categories.html', context)
    except Exception as e:
        messages.error(request, f'Error loading categories: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def add_category(request):
    try:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.owner = request.user
                category.save()
                messages.success(request, 'Category added successfully')
                return redirect('manage_categories')
            else:
                messages.error(request, 'Invalid form data')
        return redirect('manage_categories')
    except Exception as e:
        messages.error(request, f'Error adding category: {str(e)}')
        return redirect('manage_categories')

@login_required(login_url='authentication:login')
def delete_category(request, id):
    try:
        category = get_object_or_404(Category, pk=id, owner=request.user)
        if Expense.objects.filter(category=category).exists():
            messages.error(request, 'Cannot delete category with associated expenses')
        else:
            category.delete()
            messages.success(request, 'Category deleted successfully')
    except PermissionDenied:
        messages.error(request, 'You do not have permission to delete this category')
    except Exception as e:
        messages.error(request, f'Error deleting category: {str(e)}')
    return redirect('manage_categories')

@login_required(login_url='authentication:login')
def manage_budget(request):
    try:
        budgets = Budget.objects.filter(owner=request.user)
        context = {
            'budgets': budgets,
            'form': BudgetForm(user=request.user)
        }
        return render(request, 'expenses/manage_budget.html', context)
    except Exception as e:
        messages.error(request, f'Error loading budgets: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def add_budget(request):
    try:
        if request.method == 'POST':
            form = BudgetForm(request.POST, user=request.user)
            if form.is_valid():
                budget = form.save(commit=False)
                budget.owner = request.user
                budget.save()
                messages.success(request, 'Budget added successfully')
                return redirect('manage_budget')
            else:
                messages.error(request, 'Invalid form data')
        return redirect('manage_budget')
    except Exception as e:
        messages.error(request, f'Error adding budget: {str(e)}')
        return redirect('manage_budget')

@login_required(login_url='authentication:login')
def edit_budget(request, id):
    try:
        budget = get_object_or_404(Budget, pk=id, owner=request.user)
        if request.method == 'POST':
            form = BudgetForm(request.POST, instance=budget, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Budget updated successfully')
                return redirect('manage_budget')
            else:
                messages.error(request, 'Invalid form data')
        else:
            form = BudgetForm(instance=budget, user=request.user)
        context = {
            'budget': budget,
            'form': form
        }
        return render(request, 'expenses/edit_budget.html', context)
    except PermissionDenied:
        messages.error(request, 'You do not have permission to edit this budget')
        return redirect('manage_budget')
    except Exception as e:
        messages.error(request, f'Error editing budget: {str(e)}')
        return redirect('manage_budget')

@login_required(login_url='authentication:login')
def delete_budget(request, id):
    try:
        budget = get_object_or_404(Budget, pk=id, owner=request.user)
        budget.delete()
        messages.success(request, 'Budget deleted successfully')
    except PermissionDenied:
        messages.error(request, 'You do not have permission to delete this budget')
    except Exception as e:
        messages.error(request, f'Error deleting budget: {str(e)}')
    return redirect('manage_budget')

@login_required(login_url='authentication:login')
def generate_report(request):
    try:
        # Get date range from request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if not start_date or not end_date:
            messages.error(request, 'Please provide start and end dates')
            return redirect('expenses')
            
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get expenses for the date range
        expenses = Expense.objects.filter(
            owner=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        # Generate report ID
        report_id = f"report_{request.user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_id}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Category', 'Description', 'Amount'])
        
        for expense in expenses:
            writer.writerow([
                expense.date,
                expense.category.name,
                expense.description,
                expense.amount
            ])
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('expenses')

@login_required(login_url='authentication:login')
def download_report(request, report_id):
    try:
        # Validate report ID format and ownership
        user_id = report_id.split('_')[1]
        if str(request.user.id) != user_id:
            raise PermissionDenied
            
        # Get report file path
        report_path = os.path.join(settings.MEDIA_ROOT, 'reports', f"{report_id}.csv")
        
        if not os.path.exists(report_path):
            messages.error(request, 'Report not found')
            return redirect('expenses')
            
        # Serve the file
        with open(report_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{report_id}.csv"'
            return response
            
    except PermissionDenied:
        messages.error(request, 'You do not have permission to access this report')
        return redirect('expenses')
    except Exception as e:
        messages.error(request, f'Error downloading report: {str(e)}')
        return redirect('expenses')

