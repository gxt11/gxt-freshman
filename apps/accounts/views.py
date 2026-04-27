from rest_framework import generics, permissions
from django.contrib.auth.models import User

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
