from django.contrib import admin
from .models import CampusLocation, NavigationRoute, UserNavigationLog

@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type', 'latitude', 'longitude', 'is_active')
    list_filter = ('location_type', 'is_active')
    search_fields = ('name', 'address')

@admin.register(NavigationRoute)
class NavigationRouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_location', 'end_location', 'route_type', 'distance', 'duration')
    list_filter = ('route_type', 'is_active')

@admin.register(UserNavigationLog)
class UserNavigationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'created_at')
    list_filter = ('created_at',)
