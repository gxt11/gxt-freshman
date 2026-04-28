from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'locations', views.CampusLocationViewSet, basename='location')
router.register(r'routes', views.NavigationRouteViewSet, basename='route')

app_name = 'navigation'

urlpatterns = [
    path('', include(router.urls)),
    path('logs/', views.UserNavigationLogView.as_view(), name='navigation-logs'),
    path('calculate/', views.calculate_route, name='calculate-route'),
]
