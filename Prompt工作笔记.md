# PromptQ&A工作笔记 - Django+PostgreSQL+DRF架构重构

**项目**: 大学生新生智能报道助手  
**版本**: V2.0 Enterprise  
**日期**: 2026-04-25  
**开发者**: gxt11  

---

##  任务背景

**原始需求**: 
将Flask+SQLite的MVP项目重构为企业级架构

**目标架构**:
Django 5.0.4 + PostgreSQL 14+ + Django REST Framework

---

##  Prompt Q&A 记录

### Q1: 为什么要从Flask迁移到Django？

**A**: 
- Flask适合MVP快速原型，但缺乏企业级功能
- Django提供：
  - 内置Admin后台
  - ORM框架
  - 用户认证系统
  - 信号机制
  - 更完善的生态

**决策依据**:
项目需要从MVP升级到可交付的生产系统

---

### Q2: 为什么选择PostgreSQL而不是MySQL？

**A**:
- PostgreSQL优势：
  - 更好的JSON支持
  - 强大的扩展性
  - ACID合规性更强
  - 适合复杂查询
  - Django官方推荐

**对比**:
| 特性 | PostgreSQL | MySQL |
|------|-----------|-------|
| JSON支持 | 优秀 | 一般 |
| 事务 | 完整 | 部分 |
| 并发 | 高 | 中 |
| Django支持 | 一级 | 二级 |

---

### Q3: JWT和Session认证的区别？

**A**:

**Session认证**（MVP使用）:
- 服务器端存储状态
- 需要Cookie
- 不适合前后端分离
- 扩展性差

**JWT认证**（企业版使用）:
- 无状态，服务器不存储
- 适合前后端分离
- 支持跨域
- 易于扩展
- 移动端友好

**JWT工作流程**:
`
1. 用户登录  服务器返回Token
2. 客户端存储Token（LocalStorage）
3. 后续请求携带Token（Header）
4. 服务器验证Token签名
5. Token过期后刷新
`

---

### Q4: Django REST Framework是什么？

**A**:
- 基于Django的API框架
- 提供：
  - Serializer（序列化器）
  - ViewSet（视图集）
  - Router（路由器）
  - Authentication（认证）
  - Permissions（权限）
  - Pagination（分页）

**核心组件**:
`python
# Serializer - 数据转换
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# View - 业务逻辑
class StudentView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

# Router - URL路由
router = DefaultRouter()
router.register(r'students', StudentViewSet)
`

---

### Q5: 如何配置PostgreSQL数据库？

**A**:

**Step 1: 安装PostgreSQL**
`ash
# Windows
下载: https://www.postgresql.org/download/windows/
安装时设置postgres密码
`

**Step 2: 创建数据库**
`ash
createdb -U postgres freshman_db
`

**Step 3: Django配置**
`python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'freshman_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
`

**Step 4: 安装驱动**
`ash
pip install psycopg2-binary
`

---

### Q6: 如何实现JWT认证？

**A**:

**安装**:
`ash
pip install djangorestframework-simplejwt
`

**配置**:
`python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
`

**路由**:
`python
# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
]
`

**使用**:
`ash
# 登录获取Token
POST /api/auth/login/
{\"username\": \"admin\", \"password\": \"admin123\"}

# 响应
{\"access\": \"...\", \"refresh\": \"...\"}

# 使用Token访问API
GET /api/students/profile/
Header: Authorization: Bearer <access_token>
`

---

### Q7: 如何创建数据模型？

**A**:

**定义模型**:
`python
# apps/students/models.py
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    STATUS_CHOICES = (
        ('pending', '未报到'),
        ('done', '已报到'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    real_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    dorm_info = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    report_time = models.DateTimeField(null=True, blank=True)
`

**关联信号**:
`python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
`

**迁移**:
`ash
python manage.py makemigrations
python manage.py migrate
`

---

### Q8: 如何创建API接口？

**A**:

**Serializer**:
`python
# apps/students/serializers.py
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('status', 'report_time')
`

**View**:
`python
# apps/students/views.py
class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.student_profile
`

**URL**:
`python
# apps/students/urls.py
urlpatterns = [
    path('profile/', StudentProfileView.as_view()),
]
`

---

### Q9: 如何生成API文档？

**A**:

**安装**:
`ash
pip install drf-yasg
`

**配置**:
`python
# urls.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(title='新生报到API', default_version='v1'),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger')),
]
`

**访问**:
`
http://localhost:8000/swagger/
`

---

### Q10: 如何部署到生产环境？

**A**:

**Step 1: 环境变量**
`ash
# .env
SECRET_KEY=<strong-key>
DEBUG=False
DB_PASSWORD=<strong-password>
ALLOWED_HOSTS=your-domain.com
`

**Step 2: 收集静态文件**
`ash
python manage.py collectstatic
`

**Step 3: Gunicorn**
`ash
pip install gunicorn
gunicorn config.wsgi:application -w 4 -b 0.0.0.0:8000
`

**Step 4: Nginx**
`
ginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
`

---

##  关键决策点

### 决策1: 项目结构
**选择**: apps目录组织应用  
**理由**: 清晰、可扩展、便于维护

### 决策2: 认证方式
**选择**: JWT  
**理由**: 无状态、适合API、支持前后端分离

### 决策3: 数据库
**选择**: PostgreSQL  
**理由**: 功能强大、Django推荐、适合生产

### 决策4: API框架
**选择**: DRF  
**理由**: 生态完善、文档丰富、易于上手

---

##  经验总结

### 成功经验
1.  使用Django Admin快速搭建后台
2.  DRF Serializer简化数据验证
3.  JWT实现无状态认证
4.  Swagger自动生成文档

### 踩坑记录
1.  PostgreSQL连接失败  检查密码和端口
2.  迁移冲突  删除migration文件重建
3.  CORS错误  配置允许的来源
4.  Token过期  实现自动刷新

### 最佳实践
1. 使用.env管理配置
2. 遵循RESTful规范
3. 添加完善的错误处理
4. 编写单元测试
5. 使用Git版本控制

---

##  参考资料

- Django文档: https://docs.djangoproject.com/
- DRF文档: https://www.django-rest-framework.org/
- PostgreSQL文档: https://www.postgresql.org/docs/
- JWT文档: https://django-rest-framework-simplejwt.readthedocs.io/

---

**笔记版本**: V1.0  
**更新日期**: 2026-04-25  
**维护人员**: gxt11
