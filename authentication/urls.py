from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('preferences/', views.preferences_view, name='preferences'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('preferences/update/', views.update_preferences, name='update_preferences'),
    path('change-password/', views.change_password, name='change_password'),
    path('update-notifications/', views.update_notifications, name='update_notifications'),
    path('setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # Account Activation URL
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='authentication/password_reset.html',
             email_template_name='authentication/password_reset_email.html',
             subject_template_name='authentication/password_reset_subject.txt',
             success_url='/authentication/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='authentication/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='authentication/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='authentication/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]