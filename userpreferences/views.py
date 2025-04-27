from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserPreference
from django.http import JsonResponse, HttpResponse
import json
import pytz
import csv
from datetime import datetime
from io import StringIO

@login_required(login_url='/authentication/login')
def index(request):
    user_preferences = UserPreference.objects.get_or_create(user=request.user)[0]
    context = {
        'preferences': user_preferences,
        'currencies': ['USD', 'EUR', 'GBP', 'INR', 'CNY', 'JPY'],
        'themes': ['light', 'dark'],
        'languages': ['en', 'es', 'fr', 'de'],
        'timezones': ['UTC', 'US/Eastern', 'US/Pacific', 'Europe/London', 'Asia/Tokyo']
    }
    return render(request, 'userpreferences/index.html', context)

@login_required(login_url='/authentication/login')
def update_preferences(request):
    if request.method == 'POST':
        user_preferences = get_object_or_404(UserPreference, user=request.user)
        
        # Update basic preferences
        user_preferences.currency = request.POST.get('currency', user_preferences.currency)
        user_preferences.theme = request.POST.get('theme', user_preferences.theme)
        user_preferences.language = request.POST.get('language', user_preferences.language)
        user_preferences.timezone = request.POST.get('timezone', user_preferences.timezone)
        
        # Update numerical preferences
        try:
            user_preferences.monthly_budget = float(request.POST.get('monthly_budget', user_preferences.monthly_budget))
            user_preferences.savings_goal = float(request.POST.get('savings_goal', user_preferences.savings_goal))
            user_preferences.budget_alert_threshold = int(request.POST.get('budget_alert_threshold', user_preferences.budget_alert_threshold))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid numerical values provided')
            return redirect('preferences')
            
        # Update notification settings
        user_preferences.notification_enabled = request.POST.get('notification_enabled') == 'on'
        user_preferences.email_notifications = request.POST.get('email_notifications') == 'on'
        user_preferences.mobile_notifications = request.POST.get('mobile_notifications') == 'on'
        
        # Update categories if provided
        expense_categories = request.POST.get('expense_categories')
        income_categories = request.POST.get('income_categories')
        if expense_categories:
            try:
                user_preferences.expense_categories = json.loads(expense_categories)
            except json.JSONDecodeError:
                messages.error(request, 'Invalid expense categories format')
                return redirect('preferences')
                
        if income_categories:
            try:
                user_preferences.income_categories = json.loads(income_categories)
            except json.JSONDecodeError:
                messages.error(request, 'Invalid income categories format')
                return redirect('preferences')
        
        user_preferences.save()
        messages.success(request, 'Preferences updated successfully')
        return redirect('preferences')
        
    user_preferences = get_object_or_404(UserPreference, user=request.user)
    context = {
        'preferences': user_preferences
    }
    return render(request, 'userpreferences/update.html', context)

@login_required(login_url='/authentication/login')
def toggle_notification(request):
    """
    Toggle notification settings for the user
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            notification_type = request.POST.get('type')
            
            if notification_type == 'email':
                user_preferences.email_notifications = not user_preferences.email_notifications
                status = user_preferences.email_notifications
            elif notification_type == 'mobile':
                user_preferences.mobile_notifications = not user_preferences.mobile_notifications
                status = user_preferences.mobile_notifications
            else:
                user_preferences.notification_enabled = not user_preferences.notification_enabled
                status = user_preferences.notification_enabled
            
            user_preferences.save()
            return JsonResponse({
                'success': True,
                'status': status,
                'message': 'Notification settings updated successfully'
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

@login_required(login_url='/authentication/login')
def update_theme(request):
    """
    Update the user's theme preference
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            theme = request.POST.get('theme')
            
            if theme in ['light', 'dark']:
                user_preferences.theme = theme
                user_preferences.save()
                return JsonResponse({
                    'success': True,
                    'theme': theme,
                    'message': 'Theme updated successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid theme value'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required(login_url='/authentication/login')
def update_language(request):
    """
    Update the user's language preference
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            language = request.POST.get('language')
            
            # Add more languages as needed
            if language in ['en', 'es', 'fr', 'de']:
                user_preferences.language = language
                user_preferences.save()
                return JsonResponse({
                    'success': True,
                    'language': language,
                    'message': 'Language updated successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid language code'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required(login_url='/authentication/login')
def update_timezone(request):
    """
    Update the user's timezone preference
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            timezone = request.POST.get('timezone')
            
            # Validate timezone
            if timezone in pytz.all_timezones:
                user_preferences.timezone = timezone
                user_preferences.save()
                return JsonResponse({
                    'success': True,
                    'timezone': timezone,
                    'message': 'Timezone updated successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid timezone'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required(login_url='/authentication/login')
def update_budget(request):
    """
    Update the user's budget preferences
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            
            # Update monthly budget
            monthly_budget = request.POST.get('monthly_budget')
            if monthly_budget:
                try:
                    monthly_budget = float(monthly_budget)
                    if monthly_budget < 0:
                        raise ValueError("Monthly budget cannot be negative")
                    user_preferences.monthly_budget = monthly_budget
                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=400)
            
            # Update savings goal
            savings_goal = request.POST.get('savings_goal')
            if savings_goal:
                try:
                    savings_goal = float(savings_goal)
                    if savings_goal < 0:
                        raise ValueError("Savings goal cannot be negative")
                    user_preferences.savings_goal = savings_goal
                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=400)
            
            # Update budget alert threshold
            threshold = request.POST.get('budget_alert_threshold')
            if threshold:
                try:
                    threshold = int(threshold)
                    if not 0 <= threshold <= 100:
                        raise ValueError("Budget alert threshold must be between 0 and 100")
                    user_preferences.budget_alert_threshold = threshold
                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=400)
            
            user_preferences.save()
            return JsonResponse({
                'success': True,
                'message': 'Budget preferences updated successfully',
                'data': {
                    'monthly_budget': user_preferences.monthly_budget,
                    'savings_goal': user_preferences.savings_goal,
                    'budget_alert_threshold': user_preferences.budget_alert_threshold
                }
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

@login_required(login_url='/authentication/login')
def update_savings_goal(request):
    """
    Update the user's savings goal
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            savings_goal = request.POST.get('savings_goal')
            
            try:
                savings_goal = float(savings_goal)
                if savings_goal < 0:
                    raise ValueError("Savings goal cannot be negative")
                user_preferences.savings_goal = savings_goal
                user_preferences.save()
                
                return JsonResponse({
                    'success': True,
                    'savings_goal': savings_goal,
                    'message': 'Savings goal updated successfully'
                })
            except ValueError as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required(login_url='/authentication/login')
def update_categories(request):
    """
    Update the user's expense and income categories
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            
            # Update expense categories
            expense_categories = request.POST.get('expense_categories')
            if expense_categories:
                try:
                    categories = json.loads(expense_categories)
                    if not isinstance(categories, list):
                        raise ValueError("Expense categories must be a list")
                    user_preferences.expense_categories = categories
                except json.JSONDecodeError:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid expense categories format'
                    }, status=400)
            
            # Update income categories
            income_categories = request.POST.get('income_categories')
            if income_categories:
                try:
                    categories = json.loads(income_categories)
                    if not isinstance(categories, list):
                        raise ValueError("Income categories must be a list")
                    user_preferences.income_categories = categories
                except json.JSONDecodeError:
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid income categories format'
                    }, status=400)
            
            user_preferences.save()
            return JsonResponse({
                'success': True,
                'message': 'Categories updated successfully',
                'data': {
                    'expense_categories': user_preferences.expense_categories,
                    'income_categories': user_preferences.income_categories
                }
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

@login_required(login_url='/authentication/login')
def update_notification_settings(request):
    """
    Update the user's notification settings
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            
            # Update notification enabled status
            notification_enabled = request.POST.get('notification_enabled')
            if notification_enabled is not None:
                user_preferences.notification_enabled = notification_enabled == 'true'
            
            # Update email notifications
            email_notifications = request.POST.get('email_notifications')
            if email_notifications is not None:
                user_preferences.email_notifications = email_notifications == 'true'
            
            # Update mobile notifications
            mobile_notifications = request.POST.get('mobile_notifications')
            if mobile_notifications is not None:
                user_preferences.mobile_notifications = mobile_notifications == 'true'
            
            user_preferences.save()
            return JsonResponse({
                'success': True,
                'message': 'Notification settings updated successfully',
                'data': {
                    'notification_enabled': user_preferences.notification_enabled,
                    'email_notifications': user_preferences.email_notifications,
                    'mobile_notifications': user_preferences.mobile_notifications
                }
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

@login_required(login_url='/authentication/login')
def update_budget_alert(request):
    """
    Update the user's budget alert threshold
    """
    if request.method == 'POST':
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            threshold = request.POST.get('budget_alert_threshold')
            
            try:
                threshold = int(threshold)
                if not 0 <= threshold <= 100:
                    raise ValueError("Budget alert threshold must be between 0 and 100")
                user_preferences.budget_alert_threshold = threshold
                user_preferences.save()
                
                return JsonResponse({
                    'success': True,
                    'threshold': threshold,
                    'message': 'Budget alert threshold updated successfully'
                })
            except ValueError as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required(login_url='/authentication/login')
def export_preferences(request):
    """
    Export user preferences to a CSV file
    """
    try:
        user_preferences = get_object_or_404(UserPreference, user=request.user)
        
        # Create the response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="preferences_{request.user.username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Setting', 'Value'])
        
        # Write basic preferences
        writer.writerow(['Currency', user_preferences.currency])
        writer.writerow(['Theme', user_preferences.theme])
        writer.writerow(['Language', user_preferences.language])
        writer.writerow(['Timezone', user_preferences.timezone])
        
        # Write numerical preferences
        writer.writerow(['Monthly Budget', user_preferences.monthly_budget])
        writer.writerow(['Savings Goal', user_preferences.savings_goal])
        writer.writerow(['Budget Alert Threshold', user_preferences.budget_alert_threshold])
        
        # Write notification settings
        writer.writerow(['Notifications Enabled', user_preferences.notification_enabled])
        writer.writerow(['Email Notifications', user_preferences.email_notifications])
        writer.writerow(['Mobile Notifications', user_preferences.mobile_notifications])
        
        # Write categories
        writer.writerow(['Expense Categories', json.dumps(user_preferences.expense_categories)])
        writer.writerow(['Income Categories', json.dumps(user_preferences.income_categories)])
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error exporting preferences: {str(e)}')
        return redirect('preferences')

@login_required(login_url='/authentication/login')
def import_preferences(request):
    """
    Import user preferences from a CSV file
    """
    if request.method == 'POST' and request.FILES.get('preferences_file'):
        try:
            user_preferences = get_object_or_404(UserPreference, user=request.user)
            preferences_file = request.FILES['preferences_file']
            
            # Read the CSV file
            decoded_file = preferences_file.read().decode('utf-8')
            csv_reader = csv.reader(StringIO(decoded_file))
            
            # Skip header row
            next(csv_reader)
            
            # Process each row
            for row in csv_reader:
                if len(row) != 2:
                    continue
                    
                setting, value = row
                
                # Update basic preferences
                if setting == 'Currency':
                    user_preferences.currency = value
                elif setting == 'Theme' and value in ['light', 'dark']:
                    user_preferences.theme = value
                elif setting == 'Language' and value in ['en', 'es', 'fr', 'de']:
                    user_preferences.language = value
                elif setting == 'Timezone' and value in pytz.all_timezones:
                    user_preferences.timezone = value
                    
                # Update numerical preferences
                elif setting == 'Monthly Budget':
                    try:
                        user_preferences.monthly_budget = float(value)
                    except ValueError:
                        pass
                elif setting == 'Savings Goal':
                    try:
                        user_preferences.savings_goal = float(value)
                    except ValueError:
                        pass
                elif setting == 'Budget Alert Threshold':
                    try:
                        threshold = int(value)
                        if 0 <= threshold <= 100:
                            user_preferences.budget_alert_threshold = threshold
                    except ValueError:
                        pass
                        
                # Update notification settings
                elif setting == 'Notifications Enabled':
                    user_preferences.notification_enabled = value.lower() == 'true'
                elif setting == 'Email Notifications':
                    user_preferences.email_notifications = value.lower() == 'true'
                elif setting == 'Mobile Notifications':
                    user_preferences.mobile_notifications = value.lower() == 'true'
                    
                # Update categories
                elif setting == 'Expense Categories':
                    try:
                        categories = json.loads(value)
                        if isinstance(categories, list):
                            user_preferences.expense_categories = categories
                    except json.JSONDecodeError:
                        pass
                elif setting == 'Income Categories':
                    try:
                        categories = json.loads(value)
                        if isinstance(categories, list):
                            user_preferences.income_categories = categories
                    except json.JSONDecodeError:
                        pass
            
            user_preferences.save()
            messages.success(request, 'Preferences imported successfully')
            
        except Exception as e:
            messages.error(request, f'Error importing preferences: {str(e)}')
            
        return redirect('preferences')
        
    messages.error(request, 'No file was uploaded')
    return redirect('preferences')
