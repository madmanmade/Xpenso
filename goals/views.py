from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialGoal, GoalCategory
from django.utils import timezone
from django.conf import settings

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
