# 新生报到助手 v2.0 改进Prompts

## 当前版本功能

###  已实现
- 用户认证系统（JWT登录/注册）
- 学生报到信息填报
- 校园导航（地标查询+路线规划）
- 管理数据看板
- Swagger API文档
- 响应式前端页面（Bootstrap 5.3）

---

##  下一步改进Prompts

### 1. 数据库升级
```
将SQLite数据库切换到PostgreSQL生产环境：
1. 启动PostgreSQL服务
2. 在.env中配置数据库连接：
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=freshman_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
3. 运行: python manage.py migrate
```

### 2. 高德地图API集成
```
在.env中添加高德地图API密钥：
AMAP_API_KEY=你的高德地图API密钥

然后导航页面会自动调用真实的高德地图API进行路线规划，
而不是返回模拟数据。
```

### 3. 学生档案照片上传
```
实现学生头像上传功能：
1. 在StudentProfile模型添加photo字段
2. 创建文件上传API端点
3. 在仪表板页面显示和更新头像
4. 配置MEDIA_URL和MEDIA_ROOT
```

### 4. 报到流程自动化
```
添加报到流程步骤跟踪：
1. 创建ReportStep模型（步骤1:注册 -> 步骤2:填报 -> 步骤3:审核 -> 步骤4:完成）
2. 在仪表板显示进度条
3. 管理员可以审核学生报到信息
4. 完成时发送邮件通知
```

### 5. 数据可视化增强
```
管理看板添加图表：
1. 使用Chart.js添加柱状图（学院报到统计）
2. 添加饼图（报到状态分布）
3. 添加折线图（每日报到趋势）
4. 导出Excel报表功能
```

### 6. 移动端适配优化
```
优化移动端体验：
1. 添加底部Tab导航（首页/报到/导航/我的）
2. 触摸手势支持
3. 离线缓存关键数据
4. PWA支持（添加service worker）
```

### 7. 消息通知系统
```
添加站内消息和推送通知：
1. 创建Notification模型
2. 报到状态变更时发送通知
3. 导航页面添加消息提醒
4. WebSocket实时推送（Django Channels）
```

### 8. 批量导入功能
```
管理员批量导入学生数据：
1. Excel模板下载
2. 文件上传和解析
3. 数据验证和错误提示
4. 批量创建学生账号
```

### 9. 多语言支持
```
添加国际化（i18n）：
1. 配置Django翻译框架
2. 创建中英文翻译文件
3. 语言切换功能
4. 日期和数字格式化
```

### 10. 性能优化
```
生产环境优化：
1. Redis缓存热点数据
2. 数据库查询优化（select_related/prefetch_related）
3. 静态文件CDN加速
4. Gzip压缩响应
5. 数据库索引优化
```

---

##  快速启动命令

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 8000

# 访问地址
首页: http://127.0.0.1:8000/
API文档: http://127.0.0.1:8000/swagger/
管理后台: http://127.0.0.1:8000/admin/
```

---

##  环境配置

创建.env文件：
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
AMAP_API_KEY=
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

---

##  技术栈

- **后端**: Django 6.0.4 + Django REST Framework 3.15.1
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: Simple JWT
- **前端**: Bootstrap 5.3 + Font Awesome 6.0 + Axios
- **文档**: drf-yasg (Swagger)
- **部署**: Gunicorn + Nginx (生产)

---

版本: 2.0
更新日期: 2026-05-08
开发者: gxt11
