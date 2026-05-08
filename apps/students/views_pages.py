from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def student_dashboard(request):
    return render(request, 'student/dashboard.html')

def student_navigation(request):
    return render(request, 'student/navigation.html')

def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')
