from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='forecast'),
    path('generate/', views.generate_forecast, name='generate_forecast'),
    path('forecast-details/<int:forecast_id>/', views.forecast_details, name='forecast_details'),
    path('edit-forecast/<int:forecast_id>/', views.edit_forecast, name='edit_forecast'),
    path('delete-forecast/<int:forecast_id>/', views.delete_forecast, name='delete_forecast'),
    path('forecast-history/', views.forecast_history, name='forecast_history'),
    path('download-forecast/<int:forecast_id>/', views.download_forecast, name='download_forecast'),
]