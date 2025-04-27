from django.urls import path
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
]