from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.context_processors import csrf
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def activate_account(request, uidb64, token):
    try:
        # Decode the user ID from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the user exists and token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # Activate the user
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('authentication:login')
    else:
        messages.error(request, 'The activation link is invalid or has expired!')
        return redirect('authentication:login')

@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('expenses')
        
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'expenses')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password')
    
    context = {'form': form}
    context.update(csrf(request))
    return render(request, 'authentication/login.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('expenses')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully!')
            return redirect('expenses')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/authentication/login/')

@login_required
def profile_view(request):
    user = request.user
    user_profile = getattr(user, 'profile', None)
    user_preferences = getattr(user, 'preferences', None)
    return render(request, 'authentication/profile.html', {
        'user': user,
        'user_profile': user_profile,
        'user_preferences': user_preferences
    })

def preferences_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    return render(request, 'authentication/preferences.html', {
        'preferences': request.user.preferences
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user_profile = getattr(user, 'profile', None)
        # Update User model fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        # Update Profile model fields
        if user_profile:
            if 'avatar' in request.FILES:
                # Optionally delete old avatar file if needed
                if user_profile.avatar:
                    user_profile.avatar.delete(save=False)
                user_profile.avatar = request.FILES['avatar']
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

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('authentication:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return redirect('authentication:profile')

@login_required
def update_notifications(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.email_notifications = request.POST.get('email_notifications', False) == 'on'
        user_profile.budget_alerts = request.POST.get('budget_alerts', False) == 'on'
        user_profile.goal_reminders = request.POST.get('goal_reminders', False) == 'on'
        user_profile.save()
        messages.success(request, 'Notification settings updated successfully!')
    return redirect('authentication:profile')

@login_required
def setup_2fa(request):
    # This is a placeholder for 2FA setup
    # You'll need to implement proper 2FA logic using a library like django-otp
    messages.info(request, '2FA setup will be implemented in a future update.')
    return redirect('authentication:profile')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password_confirm')
        user = request.user
        
        # Verify the password before deletion
        if user.check_password(password):
            # Delete the user account
            user.delete()
            messages.success(request, 'Your account has been permanently deleted.')
            return redirect('authentication:login')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
    
    return redirect('authentication:profile')
