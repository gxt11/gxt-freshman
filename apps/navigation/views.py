from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import CampusLocation, NavigationRoute, UserNavigationLog
from .serializers import CampusLocationSerializer, NavigationRouteSerializer, UserNavigationLogSerializer, NavigationRequestSerializer

class CampusLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CampusLocation.objects.filter(is_active=True)
    serializer_class = CampusLocationSerializer
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        location_type = request.query_params.get('type')
        if location_type:
            locations = CampusLocation.objects.filter(location_type=location_type, is_active=True)
            return Response(self.get_serializer(locations, many=True).data)
        return Response({'error': 'type required'}, status=400)

class NavigationRouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NavigationRoute.objects.filter(is_active=True)
    serializer_class = NavigationRouteSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        start_id = request.query_params.get('start_id')
        end_id = request.query_params.get('end_id')
        if start_id and end_id:
            routes = NavigationRoute.objects.filter(start_location_id=start_id, end_location_id=end_id, is_active=True)
            return Response(self.get_serializer(routes, many=True).data)
        return Response({'error': 'start_id and end_id required'}, status=400)

class UserNavigationLogView(generics.ListCreateAPIView):
    serializer_class = UserNavigationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserNavigationLog.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def calculate_route(request):
    serializer = NavigationRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    from django.conf import settings
    amap_key = getattr(settings, 'AMAP_API_KEY', '')
    
    if not amap_key:
        return Response({
            'status': 'success',
            'data': {
                'distance': 1500.5,
                'duration': 18,
                'route_type': serializer.validated_data['route_type'],
                'steps': [
                    {'instruction': 'Start from origin', 'distance': 200, 'duration': 3},
                    {'instruction': 'Turn left to main road', 'distance': 800, 'duration': 10},
                    {'instruction': 'Arrive at destination', 'distance': 500, 'duration': 5},
                ]
            }
        })
    
    try:
        import requests
        origin = f"{serializer.validated_data['start_lng']},{serializer.validated_data['start_lat']}"
        destination = f"{serializer.validated_data['end_lng']},{serializer.validated_data['end_lat']}"
        
        response = requests.get(
            'https://restapi.amap.com/v5/direction/walking',
            params={'key': amap_key, 'origin': origin, 'destination': destination},
            timeout=10
        )
        return Response({'status': 'success', 'data': response.json()})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
