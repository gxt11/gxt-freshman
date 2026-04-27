from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('report/', views.ReportView.as_view(), name='student-report'),
    path('status/', views.report_status, name='report-status'),
]
