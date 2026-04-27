# Django + DRF API 完整实现指南

**状态**: 基础结构已完成，需要补充API代码  
**完成度**: 40%  

---

##  已完成

- [x] Django项目创建
- [x] 应用创建（accounts, students）
- [x] 数据模型（StudentProfile）
- [x] settings.py配置
- [x] 依赖安装

##  待完成

- [ ] Serializers（序列化器）
- [ ] Views（API视图）
- [ ] URLs（路由配置）
- [ ] Admin配置
- [ ] 数据库迁移

---

## 快速完成步骤

### Step 1: 创建 Serializers

创建文件: pps/students/serializers.py

`python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('status', 'report_time', 'created_at', 'updated_at')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('real_name', 'phone', 'dorm_info')
`

### Step 2: 创建 Views

修改文件: pps/students/views.py

`python
from rest_framework import generics, permissions, status
from rest_framework.response import Response
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
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        instance.real_name = serializer.validated_data.get('real_name', instance.real_name)
        instance.phone = serializer.validated_data.get('phone', instance.phone)
        instance.dorm_info = serializer.validated_data.get('dorm_info', instance.dorm_info)
        instance.status = 'done'
        instance.report_time = timezone.now()
        instance.save()
        
        return Response(StudentProfileSerializer(instance).data)
`

### Step 3: 创建 URLs

创建文件: pps/students/urls.py

`python
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('report/', views.ReportView.as_view(), name='student-report'),
]
`

### Step 4: 配置主路由

修改文件: config/urls.py

`python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='新生报到助手API',
        default_version='v1',
        description='Django + PostgreSQL + DRF',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/students/', include('apps.students.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
`

### Step 5: 配置 Admin

修改文件: pps/students/admin.py

`python
from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'real_name', 'phone', 'status', 'report_time')
    list_filter = ('status',)
    search_fields = ('student_id', 'real_name', 'phone')
`

### Step 6: 数据库迁移

`ash
# 使用SQLite（快速测试）
# 或使用PostgreSQL（需先创建数据库）

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
`

---

## API测试

### 1. 登录获取Token
`ash
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H \"Content-Type: application/json\" \\
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'
`

### 2. 获取档案
`ash
curl -X GET http://localhost:8000/api/students/profile/ \\
  -H \"Authorization: Bearer <token>\"
`

### 3. 提交报到
`ash
curl -X PATCH http://localhost:8000/api/students/report/ \\
  -H \"Authorization: Bearer <token>\" \\
  -H \"Content-Type: application/json\" \\
  -d '{\"real_name\":\"张三\",\"phone\":\"13800138000\",\"dorm_info\":\"1号楼302\"}'
`

---

**创建日期**: 2026-04-25  
**开发者**: gxt11
