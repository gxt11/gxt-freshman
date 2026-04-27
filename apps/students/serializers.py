from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('user', 'status', 'report_time', 'created_at', 'updated_at')
    
    def validate_phone(self, value):
        if value and len(value) != 11:
            raise serializers.ValidationError("Phone must be 11 digits")
        return value

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('real_name', 'phone', 'dorm_info')
    
    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("Phone must be 11 digits")
        return value
