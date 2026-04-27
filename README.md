# 大学生新生智能报道助手 - 企业版

> 基于 Django + PostgreSQL + Django REST Framework 的企业级新生报到管理系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.4-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.1-orange.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

##  目录

- [项目简介](#项目简介)
- [技术栈](#技术栈)
- [功能特性](#功能特性)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [API文档](#api文档)
- [数据库设计](#数据库设计)
- [部署指南](#部署指南)
- [开发文档](#开发文档)
- [常见问题](#常见问题)
- [版本历史](#版本历史)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 项目简介

大学生新生智能报道助手是一个现代化的Web应用系统，用于简化大学新生报到流程。系统从MVP版本（Flask+SQLite）升级为企业级架构，提供RESTful API接口，支持高并发访问和前后端分离部署。

### 核心功能

-  **用户认证** - JWT无状态认证，支持Token刷新
-  **信息填报** - 在线填写报到信息（姓名、电话、宿舍）
-  **状态管理** - 自动流转报到状态（pending  done）
-  **Admin后台** - Django内置管理后台，数据可视化管理
-  **API文档** - 自动生成Swagger文档，支持在线测试
-  **响应式设计** - 支持PC、平板、手机多端访问

### 架构升级

| 组件 | MVP版本 (V1.0) | 企业版本 (V2.0) |
|------|---------------|----------------|
| Web框架 | Flask 3.0 | Django 5.0.4 |
| 数据库 | SQLite | PostgreSQL 14+ |
| ORM | SQLAlchemy | Django ORM |
| API | 无（服务端渲染） | Django REST Framework |
| 认证 | Session | JWT (Simple JWT) |
| 文档 | 无 | Swagger (drf-yasg) |
| 后台 | 无 | Django Admin |

---

## 技术栈

### 后端技术

- **Django 5.0.4** - Python Web框架
- **Django REST Framework 3.15.1** - API框架
- **PostgreSQL 14+** - 关系型数据库
- **Simple JWT 5.3.1** - JWT认证
- **django-cors-headers** - CORS跨域支持
- **drf-yasg** - Swagger API文档

### 开发工具

- **Python 3.10+** - 编程语言
- **pip** - 包管理器
- **Git** - 版本控制
- **VS Code / PyCharm** - IDE

---

## 功能特性

### 用户端

- 用户登录（JWT认证）
- 查看个人档案
- 填写报到信息
- 查询报到状态
- 修改个人信息

### 管理端

- 用户管理
- 学生档案管理
- 报到数据统计
- 数据导入/导出
- 权限管理

### API特性

- RESTful接口设计
- JWT Token认证
- 请求数据验证
- 分页和过滤
- 错误处理
- Swagger文档

---

## 项目结构

`
gxt-freshman/

  config/                      # Django项目配置
    __init__.py
    settings.py                 # 核心配置
    urls.py                     # 主路由
    wsgi.py                     # WSGI入口
    asgi.py                     # ASGI入口

  apps/                        # 应用模块
    __init__.py
    accounts/                   # 用户认证应用
       models.py
       serializers.py
       views.py
       urls.py
       admin.py
   
    students/                   # 学生报到应用
        models.py               # 数据模型
        serializers.py          # 序列化器
        views.py                # API视图
        urls.py                 # API路由
        admin.py                # Admin配置

  templates/                   # HTML模板
  static/                      # 静态文件
  staticfiles/                 # 收集的静态文件

 manage.py                       # Django管理脚本
 requirements.txt                # Python依赖
 .env                            # 环境变量（不提交）
 .env.example                    # 环境变量示例
 .gitignore                      # Git忽略配置

  docs/                        # 文档目录
     技术方案书.md
     用户使用说明书.md
     API接口文档.md
     API实现指南.md
     Prompt工作笔记.md
`

---

## 快速开始

### 环境要求

- Python 3.10+
- PostgreSQL 14+
- pip 21.0+
- Git 2.30+

### 安装步骤

#### 1. 克隆项目

`ash
cd D:\freshman-assistant\gxt-freshman
`

#### 2. 安装PostgreSQL

下载地址: https://www.postgresql.org/download/windows/

安装后创建数据库：
`ash
createdb -U postgres freshman_db
`

#### 3. 安装依赖

`ash
pip install -r requirements.txt
`

#### 4. 配置环境变量

复制环境变量示例文件：
`ash
copy .env.example .env
`

编辑 .env 文件：
`env
# Django配置
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL数据库
DB_NAME=freshman_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# CORS配置
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
`

#### 5. 数据库迁移

`ash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户（Admin后台）
python manage.py createsuperuser
`

#### 6. 启动开发服务器

`ash
python manage.py runserver
`

访问地址：
-  **API文档**: http://localhost:8000/swagger/
-  **Admin后台**: http://localhost:8000/admin/
-  **API根目录**: http://localhost:8000/api/

---

## API文档

### 认证接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/auth/login/ | 登录获取Token |  |
| POST | /api/auth/refresh/ | 刷新Token |  |

### 学生报到接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /api/students/profile/ | 获取档案 |  |
| PUT | /api/students/profile/ | 更新档案 |  |
| PATCH | /api/students/report/ | 提交报到 |  |

### 快速测试

#### 1. 登录获取Token

`ash
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H \"Content-Type: application/json\" \\
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'
`

**响应**:
`json
{
  \"access\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...\",
  \"refresh\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...\"
}
`

#### 2. 获取学生档案

`ash
curl -X GET http://localhost:8000/api/students/profile/ \\
  -H \"Authorization: Bearer <access_token>\"
`

#### 3. 提交报到信息

`ash
curl -X PATCH http://localhost:8000/api/students/report/ \\
  -H \"Authorization: Bearer <access_token>\" \\
  -H \"Content-Type: application/json\" \\
  -d '{\"real_name\":\"张三\",\"phone\":\"13800138000\",\"dorm_info\":\"1号楼302\"}'
`

 **完整API文档**: 查看 [API接口文档.md](API接口文档.md)

---

## 数据库设计

### 核心表

#### auth_user（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 主键 |
| username | Varchar(150) | 用户名（学号） |
| password | Varchar(128) | 密码（加密） |
| email | Varchar(254) | 邮箱 |
| is_active | Boolean | 是否激活 |

#### student_profiles（学生档案表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 主键 |
| user_id | Integer (FK, Unique) | 外键auth_user |
| student_id | Varchar(20) | 学号 |
| real_name | Varchar(50) | 真实姓名 |
| phone | Varchar(20) | 联系电话 |
| dorm_info | Varchar(100) | 宿舍信息 |
| status | Varchar(20) | 状态（pending/done） |
| report_time | Timestamp | 报到时间 |

### 表关系

`
auth_user (1)  (1) student_profiles
      一对一关系，通过user_id外键关联
      级联删除：ON DELETE CASCADE
`

 **详细设计**: 查看 [技术方案书.md](技术方案书.md)

---

## 部署指南

### 开发环境

`ash
python manage.py runserver
`

### 生产环境

#### 1. 配置环境变量

`env
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_PASSWORD=<strong-password>
`

#### 2. 收集静态文件

`ash
python manage.py collectstatic
`

#### 3. 使用Gunicorn

`ash
pip install gunicorn
gunicorn config.wsgi:application -w 4 -b 0.0.0.0:8000
`

#### 4. Nginx配置

`
ginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host System.Management.Automation.Internal.Host.InternalHost;
        proxy_set_header X-Real-IP ;
    }
    
    location /static/ {
        alias /var/www/staticfiles/;
    }
}
`

 **详细部署**: 查看 [用户使用说明书.md](用户使用说明书.md)

---

## 开发文档

### 本地开发工作流

`ash
# 1. 创建分支
git checkout -b feature/your-feature

# 2. 开发功能
# ... 编写代码 ...

# 3. 运行测试
python manage.py test

# 4. 提交代码
git add .
git commit -m \"feat: add new feature\"
git push origin feature/your-feature

# 5. 创建Pull Request
`

### 代码规范

- 遵循PEP 8规范
- 使用4个空格缩进
- 函数和类添加文档字符串
- 变量名使用snake_case
- 常量使用UPPER_CASE

### 提交信息规范

`
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建/工具链相关
`

 **开发笔记**: 查看 [Prompt工作笔记.md](Prompt工作笔记.md)

---

## 常见问题

### Q1: 数据库连接失败？

**错误**: could not connect to server

**解决**:
1. 检查PostgreSQL服务是否启动
2. 检查.env中的DB_PASSWORD
3. 测试连接: psql -U postgres -d freshman_db

### Q2: 迁移失败？

**错误**: django.db.utils.ProgrammingError

**解决**:
`ash
# 删除数据库重新创建
dropdb freshman_db
createdb freshman_db
python manage.py migrate
`

### Q3: Token过期？

**错误**: 401 Unauthorized

**解决**: 使用refresh接口获取新Token

### Q4: CORS错误？

**错误**: Access-Control-Allow-Origin

**解决**: 在.env中添加前端域名到CORS_ALLOWED_ORIGINS

 **更多问题**: 查看 [用户使用说明书.md](用户使用说明书.md)

---

## 版本历史

### V2.0（当前版本）- 2026-04-25

-  Django 5.0.4框架
-  PostgreSQL数据库
-  Django REST Framework
-  JWT认证
-  Swagger API文档
-  Django Admin后台
-  CORS跨域支持

### V1.0（MVP版本）

- Flask框架
- SQLite数据库
- Session认证
- 服务端渲染

---

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (git checkout -b feature/AmazingFeature)
3. 提交更改 (git commit -m 'feat: add some AmazingFeature')
4. 推送到分支 (git push origin feature/AmazingFeature)
5. 开启Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 联系方式

- **开发者**: gxt11
- **项目地址**: D:\freshman-assistant\gxt-freshman
- **创建日期**: 2026-04-25

---

## 致谢

- [Django](https://www.djangoproject.com/) - Web框架
- [Django REST Framework](https://www.django-rest-framework.org/) - API框架
- [PostgreSQL](https://www.postgresql.org/) - 数据库
- [Bootstrap](https://getbootstrap.com/) - 前端框架

---

 如果这个项目对你有帮助，请给个Star！
