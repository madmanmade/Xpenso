"""
URL configuration for expensetracker_enhanced project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),  # Main expense tracking functionality
    path('authentication/', include('authentication.urls')),  # User authentication & registration
    path('preferences/', include('userpreferences.urls')),  # User preferences like currency, theme
    path('income/', include('userincome.urls')),  # Income tracking
    path('goals/', include('goals.urls')),  # Financial goals setting & tracking
    path('forecast/', include('expense_forecast.urls')),  # Expense prediction & analysis
    path('reports/', include('report_generation.urls')),  # Generate financial reports
    path('api/', include('api.urls')),  # REST API endpoints
    path('dashboard/', RedirectView.as_view(url='/', permanent=True)),  # Redirect dashboard to home
    path('categories/', include('expenses.urls')),  # Expense categories management
    path('analytics/', include('analytics.urls')),  # Advanced analytics & insights
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Enable debug toolbar in development
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    # Add custom error handlers in development for testing
    from django.conf.urls import handler404, handler500
    from expenses.views import custom_404, custom_500
    
    handler404 = 'expenses.views.custom_404'
    handler500 = 'expenses.views.custom_500'
