from django.urls import path
from . import views

urlpatterns = [
    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/availability/create/', views.create_availability, name='create_availability'),
    path('admin/appointments/', views.all_appointments, name='all_appointments'),
    path('admin/availability/list/', views.availability_list_admin, name='availability_list_admin'),

    # Appointment logic
    path('', views.availability_list, name='availability_list'),
    path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
    path('my/', views.my_appointments, name='my_appointments'),
]