from django.urls import path
from . import views

urlpatterns = [
    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Appointment logic
    path('', views.availability_list, name='availability_list'),
    path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
    path('my/', views.my_appointments, name='my_appointments'),

    # Admin availability creation
    path('availability/create/', views.admin_create_availability, name='admin_create_availability'),
]