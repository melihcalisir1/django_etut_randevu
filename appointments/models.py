from django.db import models
from django.conf import settings
from users.models import User, Role

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Availability(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__name': 'Admin'},
        related_name='availabilities'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    quota = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time} (Admin: {self.admin.username})"

class Appointment(models.Model):
    availability = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role__name': 'Student'},
        related_name='appointments'
    )
    branches = models.ManyToManyField(Branch)
    status = models.CharField(max_length=20, choices=[
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ], default='approved')
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_appointments'
    )
    cancel_reason = models.TextField(blank=True, null=True)

    def __str__(self):
            return f"{self.student.username} - {self.availability.date} ({self.status})"