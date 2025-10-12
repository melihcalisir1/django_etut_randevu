from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Anasayfa yönlendirmesi (root)
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='root_redirect'),
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
    path('users/', include('users.urls')),
]
