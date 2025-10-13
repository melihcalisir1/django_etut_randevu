from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Availability, Appointment, Branch
from users.models import User
from datetime import timedelta, date, datetime
from django.utils import timezone
from django.core.paginator import Paginator

# -------------------------------
# 🌍 Dashboardlar
# -------------------------------

def is_admin(user):
    return user.is_authenticated and user.role and user.role.name.lower() == 'admin'

@login_required
def student_dashboard(request):
    """Öğrencinin ana paneli"""
    return render(request, 'appointments/student_dashboard.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_availabilities = Availability.objects.count()
    total_appointments = Appointment.objects.count()
    total_students = User.objects.filter(role__name='Student').count()

    return render(request, 'appointments/admin_dashboard.html', {
        'total_availabilities': total_availabilities,
        'total_appointments': total_appointments,
        'total_students': total_students,
    })


# Uygunluk listesini göster
def availability_list(request):
    availabilities = Availability.objects.all().order_by('date', 'start_time')
    return render(request, 'appointments/availability_list.html', {
        'availabilities': availabilities
    })

# Randevu oluşturma
@login_required
def book_appointment(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id)
    branches = Branch.objects.all()
    student = request.user

    if request.method == 'POST':

        existing = Appointment.objects.filter(
            availability=availability, student=student
        ).exists()

        if existing:
                messages.warning(request, "Bu saat için zaten bir randevunuz var.")
                return redirect('availability_list')

        selected_branches = request.POST.getlist('branches')
        appointment = Appointment.objects.create(
            availability=availability,
            student=student
        )
        appointment.branches.set(selected_branches)
        appointment.save()

        messages.success(request, "Randevunuz başarıyla oluşturuldu 🎉")
        return redirect('availability_list')

    return render(request, 'appointments/book_appointment.html', {
        'availability': availability,
        'branches': branches
    })

@login_required
def my_appointments(request):
    # Sadece giriş yapan öğrencinin randevularını çek
    appointments = (
        Appointment.objects
        .filter(student=request.user)
        .select_related('availability')
        .prefetch_related('branches')
    )

    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments
    })

def is_admin(user):
    return user.is_authenticated and user.role and user.role.name == 'Admin'

@user_passes_test(is_admin)
def create_availability(request):
    if request.method == 'POST':
        mode = request.POST.get('mode')

        if mode == 'single':
            # Tek bi availability oluşturma
            date_str = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            quota = request.POST.get('quota')
            note = request.POST.get('note')

            Availability.objects.create(
                admin=request.user,
                date=date_str,
                start_time=start_time,
                end_time=end_time,
                quota=quota,
                note=note
            )
            messages.success(request, "Tekil uygunluk başarıyla oluşturuldu ✅")
            return redirect('admin_create_availability')

        elif mode == 'bulk':
            # Toplu oluşturma (önümüzdeki 50 gün)
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            quota = request.POST.get('quota')
            note = request.POST.get('note')

            today = date.today()
            for i in range(50):
                day = today + timedelta(days=i)
                Availability.objects.create(
                    admin=request.user,
                    date=day,
                    start_time=start_time,
                    end_time=end_time,
                    quota=quota,
                    note=note
                )
            messages.success(request, "Önümüzdeki 50 gün için uygunluklar oluşturuldu ✅")
            return redirect('admin_create_availability')
    return render(request, 'appointments/admin_create_availability.html')

@user_passes_test(is_admin)
def all_appointments(request):
    appointments = Appointment.objects.select_related('availability', 'student').all().order_by('-id')
    return render(request, 'appointments/all_appointments.html', {'appointments': appointments})

@user_passes_test(is_admin)
def availability_list_admin(request):
    """Admin tarafında uygunlukları listele + gelişmiş filtreleme"""
    availabilities = Availability.objects.all().order_by('-date', 'start_time')

    # 🔍 Filtre verilerini al
    single_date = request.GET.get('single_date')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_note = request.GET.get('note')

    # 🔧 Filtre uygulamaları
    if single_date:
        availabilities = availabilities.filter(date=single_date)
    elif start_date and end_date:
        availabilities = availabilities.filter(date__range=[start_date, end_date])
    elif start_date:
        availabilities = availabilities.filter(date__gte=start_date)
    elif end_date:
        availabilities = availabilities.filter(date__lte=end_date)

    if search_note:
        availabilities = availabilities.filter(note__icontains=search_note)

    # 🔢 Sayfalama
    paginator = Paginator(availabilities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'appointments/admin_availability_list.html', {
        'page_obj': page_obj,
        'single_date': single_date,
        'start_date': start_date,
        'end_date': end_date,
        'search_note': search_note
    })