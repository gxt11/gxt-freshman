from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.students.views_pages import login_page, register_page, student_dashboard, student_navigation, admin_dashboard

def home(request):
    return render(request, 'home.html')

schema_view = get_schema_view(
    openapi.Info(
        title="Freshman Report API",
        default_version='v1',
        description="Django + PostgreSQL + DRF"),
    public=True)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('student/dashboard/', student_dashboard, name='student-dashboard'),
    path('student/navigation/', student_navigation, name='student-navigation'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/students/', include('apps.students.urls')),
    path('api/navigation/', include('apps.navigation.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
