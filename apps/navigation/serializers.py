from rest_framework import serializers
from .models import CampusLocation, NavigationRoute, UserNavigationLog

class CampusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusLocation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class NavigationRouteSerializer(serializers.ModelSerializer):
    start_location = CampusLocationSerializer(read_only=True)
    end_location = CampusLocationSerializer(read_only=True)
    start_location_id = serializers.PrimaryKeyRelatedField(queryset=CampusLocation.objects.all(), source='start_location', write_only=True)
    end_location_id = serializers.PrimaryKeyRelatedField(queryset=CampusLocation.objects.all(), source='end_location', write_only=True)
    
    class Meta:
        model = NavigationRoute
        fields = '__all__'
        read_only_fields = ('created_at',)

class UserNavigationLogSerializer(serializers.ModelSerializer):
    route = NavigationRouteSerializer(read_only=True)
    
    class Meta:
        model = UserNavigationLog
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class NavigationRequestSerializer(serializers.Serializer):
    start_lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    start_lng = serializers.DecimalField(max_digits=10, decimal_places=7)
    end_lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    end_lng = serializers.DecimalField(max_digits=10, decimal_places=7)
    route_type = serializers.ChoiceField(choices=['walking', 'bicycle', 'shuttle'], default='walking')
