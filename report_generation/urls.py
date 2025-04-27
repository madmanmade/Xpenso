from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports'),
    path('generate/', views.generate_report, name='generate_report'),
    path('download/<str:report_id>/', views.download_report, name='download_report'), 
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('report-details/<int:report_id>/', views.report_details, name='report_details'),
    path('delete-report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('filter-reports/', views.filter_reports, name='filter_reports'),
    path('share-report/<int:report_id>/', views.share_report, name='share_report'),
    path('schedule-report/', views.schedule_report, name='schedule_report'),
    path('report-history/', views.report_history, name='report_history'),
    path('report-templates/', views.report_templates, name='report_templates'),
    path('save-template/', views.save_template, name='save_template'),
    path('edit-template/<int:template_id>/', views.edit_template, name='edit_template'),
    path('delete-template/<int:template_id>/', views.delete_template, name='delete_template'),
]