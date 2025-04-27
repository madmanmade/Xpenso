from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('expenses')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authentication/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    return render(request, 'authentication/profile.html', {
        'user_profile': request.user.profile,
        'user_preferences': request.user.preferences
    })

def preferences_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    return render(request, 'authentication/preferences.html', {
        'preferences': request.user.preferences
    })

def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.currency_preference = request.POST.get('currency_preference', user_profile.currency_preference)
        user_profile.monthly_budget = request.POST.get('monthly_budget', user_profile.monthly_budget)
        user_profile.notification_enabled = request.POST.get('notification_enabled', False) == 'on'
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('authentication:profile')
    
    return redirect('authentication:profile')

def update_preferences(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    if request.method == 'POST':
        preferences = request.user.preferences
        preferences.dark_mode = request.POST.get('dark_mode', False) == 'on'
        preferences.language = request.POST.get('language', preferences.language)
        preferences.email_notifications = request.POST.get('email_notifications', False) == 'on'
        preferences.push_notifications = request.POST.get('push_notifications', False) == 'on'
        preferences.weekly_report = request.POST.get('weekly_report', False) == 'on'
        preferences.monthly_report = request.POST.get('monthly_report', False) == 'on'
        preferences.save()
        messages.success(request, 'Preferences updated successfully!')
        return redirect('authentication:preferences')
    
    return redirect('authentication:preferences')
