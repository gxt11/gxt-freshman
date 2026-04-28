from django.db import models
from django.contrib.auth.models import User

class CampusLocation(models.Model):
    LOCATION_TYPE_CHOICES = (
        ('gate', '校门'),
        ('building', '教学楼'),
        ('dorm', '宿舍楼'),
        ('canteen', '食堂'),
        ('library', '图书馆'),
        ('office', '办公楼'),
        ('other', '其他'),
    )
    
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    address = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    image = models.URLField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'campus_locations'
        verbose_name = 'Campus Location'
    
    def __str__(self):
        return f'{self.name} ({self.location_type})'


class NavigationRoute(models.Model):
    ROUTE_TYPE_CHOICES = (
        ('walking', 'Walking'),
        ('bicycle', 'Bicycle'),
        ('shuttle', 'Shuttle Bus'),
    )
    
    name = models.CharField(max_length=100)
    start_location = models.ForeignKey(CampusLocation, on_delete=models.CASCADE, related_name='start_routes')
    end_location = models.ForeignKey(CampusLocation, on_delete=models.CASCADE, related_name='end_routes')
    route_type = models.CharField(max_length=20, choices=ROUTE_TYPE_CHOICES, default='walking')
    distance = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField()
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'navigation_routes'
        verbose_name = 'Navigation Route'
    
    def __str__(self):
        return f'{self.start_location} -> {self.end_location}'


class UserNavigationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='navigation_logs')
    route = models.ForeignKey(NavigationRoute, on_delete=models.SET_NULL, null=True)
    start_lat = models.DecimalField(max_digits=10, decimal_places=7)
    start_lng = models.DecimalField(max_digits=10, decimal_places=7)
    end_lat = models.DecimalField(max_digits=10, decimal_places=7)
    end_lng = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_navigation_logs'
        verbose_name = 'Navigation Log'
    
    def __str__(self):
        return f'{self.user.username} - {self.created_at}'
