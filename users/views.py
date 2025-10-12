from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Role
from users.models import User

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Rol kontrolü
            if user.role and user.role.name.lower() == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
            return redirect('login')
    return render(request, 'users/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')
