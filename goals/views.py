from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialGoal, GoalCategory, SavingsGoal
from django.utils import timezone
from django.conf import settings
from .forms import SavingsGoalForm
from django.db.models import Sum

@login_required(login_url='/authentication/login')
def index(request):
    goals = FinancialGoal.objects.filter(user=request.user).order_by('deadline')
    context = {
        'goals': goals,
        'active_goals': goals.filter(status='ACTIVE'),
        'completed_goals': goals.filter(status='COMPLETED'),
        'abandoned_goals': goals.filter(status='ABANDONED')
    }
    return render(request, 'goals/index.html', context)

@login_required(login_url='/authentication/login')
def add_goal(request):
    categories = GoalCategory.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        target_amount = request.POST.get('target_amount')
        deadline = request.POST.get('deadline')
        category_id = request.POST.get('category')

        try:
            deadline_date = timezone.datetime.strptime(deadline, '%Y-%m-%d').date()
            if deadline_date <= timezone.now().date():
                messages.error(request, 'Deadline must be in the future')
                return redirect('add_goal')

            category = GoalCategory.objects.get(id=category_id) if category_id else None
            
            goal = FinancialGoal.objects.create(
                title=title,
                description=description,
                target_amount=target_amount,
                deadline=deadline_date,
                category=category,
                user=request.user
            )
            messages.success(request, 'Goal added successfully')
            return redirect('goals')
        except Exception as e:
            messages.error(request, f'Error creating goal: {str(e)}')
            return redirect('add_goal')

    context = {'categories': categories}
    return render(request, 'goals/add_goal.html', context)

@login_required(login_url='/authentication/login')
def edit_goal(request, id):
    goal = get_object_or_404(FinancialGoal, id=id, user=request.user)
    categories = GoalCategory.objects.all()

    if request.method == 'POST':
        try:
            goal.title = request.POST.get('title')
            goal.description = request.POST.get('description')
            goal.target_amount = request.POST.get('target_amount')
            
            deadline = request.POST.get('deadline')
            deadline_date = timezone.datetime.strptime(deadline, '%Y-%m-%d').date()
            if deadline_date <= timezone.now().date():
                messages.error(request, 'Deadline must be in the future')
                return redirect('edit_goal', id=id)
            
            goal.deadline = deadline_date
            category_id = request.POST.get('category')
            goal.category = GoalCategory.objects.get(id=category_id) if category_id else None
            goal.status = request.POST.get('status')
            
            goal.save()
            messages.success(request, 'Goal updated successfully')
            return redirect('goals')
        except Exception as e:
            messages.error(request, f'Error updating goal: {str(e)}')
            return redirect('edit_goal', id=id)

    context = {
        'goal': goal,
        'categories': categories
    }
    return render(request, 'goals/edit_goal.html', context)

@login_required(login_url='/authentication/login')
def delete_goal(request, id):
    goal = get_object_or_404(FinancialGoal, id=id, user=request.user)
    try:
        goal.delete()
        messages.success(request, 'Goal deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting goal: {str(e)}')
    return redirect('goals')

@login_required(login_url='/authentication/login')
def goal_details(request, id):
    goal = get_object_or_404(FinancialGoal, id=id, user=request.user)
    
    # Calculate progress percentage
    progress = 0
    if goal.target_amount > 0:
        progress = (goal.current_amount / goal.target_amount) * 100
        progress = min(100, round(progress, 2))
    
    # Calculate days remaining
    days_remaining = (goal.deadline - timezone.now().date()).days
    
    context = {
        'goal': goal,
        'progress': progress,
        'days_remaining': days_remaining
    }
    return render(request, 'goals/goal_details.html', context)

@login_required(login_url='/authentication/login')
def update_goal_progress(request, id):
    if request.method == 'POST':
        goal = get_object_or_404(FinancialGoal, id=id, user=request.user)
        try:
            amount = float(request.POST.get('amount', 0))
            if amount <= 0:
                messages.error(request, 'Please enter a valid positive amount')
                return redirect('goal_details', id=id)
                
            goal.current_amount += amount
            
            if goal.current_amount >= goal.target_amount:
                goal.status = 'Completed'
                messages.success(request, 'Congratulations! Goal has been achieved!')
            else:
                messages.success(request, f'Progress updated successfully! Added ${amount}')
                
            goal.save()
            
        except Exception as e:
            messages.error(request, f'Error updating progress: {str(e)}')
            
        return redirect('goal_details', id=id)
    return redirect('goals')

@login_required(login_url='authentication:login')
def savings_goals_list(request):
    goals = SavingsGoal.objects.filter(owner=request.user).order_by('-created_at')
    total_savings = sum(goal.current_amount for goal in goals)
    total_target = sum(goal.target_amount for goal in goals)
    
    context = {
        'goals': goals,
        'total_savings': total_savings,
        'total_target': total_target,
        'overall_progress': (total_savings / total_target * 100) if total_target > 0 else 0
    }
    return render(request, 'goals/savings_goals.html', context)

@login_required(login_url='authentication:login')
def add_savings_goal(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.owner = request.user
            # Ensure current_amount is not None or blank
            if not goal.current_amount:
                goal.current_amount = 0
            goal.save()
            messages.success(request, 'Savings goal created successfully!')
            return redirect('savings_goals_list')
    else:
        form = SavingsGoalForm()
    
    return render(request, 'goals/add_savings_goal.html', {'form': form})

@login_required(login_url='authentication:login')
def edit_savings_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, owner=request.user)
    
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Savings goal updated successfully!')
            return redirect('savings_goals_list')
    else:
        form = SavingsGoalForm(instance=goal)
    
    return render(request, 'goals/edit_savings_goal.html', {'form': form, 'goal': goal})

@login_required(login_url='authentication:login')
def delete_savings_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, owner=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Savings goal deleted successfully!')
    return redirect('savings_goals_list')

@login_required(login_url='authentication:login')
def update_savings_amount(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, owner=request.user)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount < 0:
                messages.error(request, 'Amount cannot be negative')
            else:
                goal.current_amount = amount
                goal.save()
                messages.success(request, 'Savings amount updated successfully!')
        except ValueError:
            messages.error(request, 'Please enter a valid amount')
    
    return redirect('savings_goals_list')
