from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from .models import StudentProfile
from .serializers import StudentProfileSerializer, ReportSerializer

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.student_profile

class ReportView(generics.UpdateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.student_profile
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'done':
            return Response({'error': 'Already reported'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        instance.real_name = serializer.validated_data.get('real_name', instance.real_name)
        instance.phone = serializer.validated_data.get('phone', instance.phone)
        instance.dorm_info = serializer.validated_data.get('dorm_info', instance.dorm_info)
        instance.status = 'done'
        instance.report_time = timezone.now()
        instance.save()
        
        return Response(StudentProfileSerializer(instance).data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def report_status(request):
    try:
        profile = request.user.student_profile
        return Response({
            'status': profile.status,
            'message': 'Done' if profile.status == 'done' else 'Pending',
            'report_time': profile.report_time,
            'can_report': profile.status == 'pending'
        })
    except StudentProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
