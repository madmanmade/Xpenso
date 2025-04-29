from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.context_processors import csrf
from django.urls import reverse

# Create your views here.

@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password')
    
    context = {'form': form}
    context.update(csrf(request))
    return render(request, 'authentication/login.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully!')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/authentication/login/')

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
