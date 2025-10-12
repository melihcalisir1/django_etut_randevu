from django.contrib import admin
from .models import Branch, Availability, Appointment

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'quota', 'admin')
    exclude = ('admin',)

    def save_model(self, request, obj, form, change):
        if not obj.admin_id:
            obj.admin = request.user # oturumdaki kullanıcıyı ata
        super().save_model(request, obj, form, change)

admin.site.register(Branch)
admin.site.register(Appointment)