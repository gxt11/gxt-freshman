from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'real_name', 'phone', 'status', 'report_time')
    list_filter = ('status',)
    search_fields = ('student_id', 'real_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
