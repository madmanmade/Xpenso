from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import UserIncome, Source
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
from django.core.exceptions import PermissionDenied
import csv
from datetime import datetime
from django.db.models import Q

@login_required(login_url='/authentication/login')
def index(request):
    incomes = UserIncome.objects.filter(owner=request.user).select_related('source')
    paginator = Paginator(incomes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'  # Default currency
        
    context = {
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'userincome/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.filter(owner=request.user)
    context = {
        'sources': sources,
        'values': request.POST
    }
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source_id = request.POST.get('source')
        date = request.POST.get('income_date')
        notes = request.POST.get('notes', '')
        receipt = request.FILES.get('receipt')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/add_income.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'userincome/add_income.html', context)
            
        try:
            source = Source.objects.get(id=source_id, owner=request.user)
        except Source.DoesNotExist:
            messages.error(request, 'Invalid source selected')
            return render(request, 'userincome/add_income.html', context)

        try:
            income = UserIncome.objects.create(
                owner=request.user,
                amount=amount,
                date=date,
                source=source,
                description=description,
                notes=notes,
                receipt=receipt
            )
            messages.success(request, 'Income added successfully')
            return redirect('income')
        except Exception as e:
            messages.error(request, f'Error adding income: {str(e)}')
            return render(request, 'userincome/add_income.html', context)
        
    return render(request, 'userincome/add_income.html', context)

@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    sources = Source.objects.filter(owner=request.user)
    
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source_id = request.POST.get('source')
        date = request.POST.get('income_date')
        notes = request.POST.get('notes', '')
        receipt = request.FILES.get('receipt')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/edit_income.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'userincome/edit_income.html', context)

        try:
            source = Source.objects.get(id=source_id, owner=request.user)
            
            income.amount = amount
            income.date = date
            income.source = source
            income.description = description
            income.notes = notes
            if receipt:
                income.receipt = receipt
            income.save()
            
            messages.success(request, 'Income updated successfully')
            return redirect('income')
            
        except Exception as e:
            messages.error(request, f'Error updating income: {str(e)}')
            return render(request, 'userincome/edit_income.html', context)
        
    return render(request, 'userincome/edit_income.html', context)

@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    try:
        income.delete()
        messages.success(request, 'Income deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting income: {str(e)}')
    return redirect('income')

@login_required(login_url='/authentication/login')
def income_source(request):
    sources = Source.objects.filter(owner=request.user)
    context = {
        'sources': sources
    }
    return render(request, 'userincome/income_source.html', context)

@login_required(login_url='/authentication/login') 
def add_source(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, 'Source name is required')
            return redirect('income-source')
            
        try:
            Source.objects.create(owner=request.user, name=name)
            messages.success(request, 'Income source added successfully')
        except Exception as e:
            messages.error(request, f'Error adding source: {str(e)}')
        return redirect('income-source')
        
    return render(request, 'userincome/add_source.html')

@login_required(login_url='/authentication/login')
def edit_source(request, id):
    source = get_object_or_404(Source, pk=id, owner=request.user)
    context = {
        'source': source
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, 'Source name is required')
            return render(request, 'userincome/edit_source.html', context)
            
        try:
            source.name = name
            source.save()
            messages.success(request, 'Income source updated successfully')
        except Exception as e:
            messages.error(request, f'Error updating source: {str(e)}')
        return redirect('income-source')
        
    return render(request, 'userincome/edit_source.html', context)

@login_required(login_url='/authentication/login')
def delete_source(request, id):
    source = get_object_or_404(Source, pk=id, owner=request.user)
    try:
        source.delete()
        messages.success(request, 'Income source deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting source: {str(e)}')
    return redirect('income-source')

@login_required(login_url='/authentication/login')
def income_summary(request):
    incomes = UserIncome.objects.filter(owner=request.user)
    total = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get income by source
    source_summary = incomes.values('source__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Get monthly summary
    monthly_summary = incomes.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('-month')
    
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'
    
    context = {
        'total': total,
        'source_summary': source_summary,
        'monthly_summary': monthly_summary,
        'currency': currency
    }
    return render(request, 'userincome/income_summary.html', context)

@login_required(login_url='/authentication/login')
def income_detail(request, id):
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'
        
    context = {
        'income': income,
        'currency': currency
    }
    return render(request, 'userincome/income_detail.html', context)

def search_income(request):
    """
    Search for income entries based on user input.
    Supports searching by source, description, amount range, and date range.
    Returns JSON response with matching income entries.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        search_str = data.get('searchText', '').strip()
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        min_amount = data.get('minAmount')
        max_amount = data.get('maxAmount')
        
        # Base queryset
        income_list = UserIncome.objects.filter(owner=request.user)
        
        # Apply filters based on search parameters
        if search_str:
            income_list = income_list.filter(
                Q(source__icontains=search_str) |
                Q(description__icontains=search_str)
            )
        
        if start_date:
            income_list = income_list.filter(date__gte=start_date)
        
        if end_date:
            income_list = income_list.filter(date__lte=end_date)
        
        if min_amount is not None:
            income_list = income_list.filter(amount__gte=min_amount)
        
        if max_amount is not None:
            income_list = income_list.filter(amount__lte=max_amount)
        
        # Order results by date
        income_list = income_list.order_by('-date')
        
        # Serialize the results
        data = []
        for income in income_list:
            data.append({
                'id': income.id,
                'amount': str(income.amount),
                'source': income.source,
                'description': income.description,
                'date': income.date.strftime('%Y-%m-%d'),
                'category': income.category.name if income.category else None
            })
        
        return JsonResponse({'results': data})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
