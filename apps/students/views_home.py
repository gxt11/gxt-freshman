from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    """首页视图"""
    return render(request, 'home.html')

def api_home(request):
    """API根路径"""
    return JsonResponse({
        'name': 'Freshman Report System API',
        'version': '2.0',
        'endpoints': {
            'auth': '/api/auth/login/',
            'students': '/api/students/profile/',
            'navigation': '/api/navigation/locations/',
            'docs': '/swagger/'
        }
    })
