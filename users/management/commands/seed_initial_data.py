from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import Role, User


class Command(BaseCommand):
    help = 'Başlangıç verilerini (roller ve örnek kullanıcılar) oluşturur.'

    @transaction.atomic
    def handle(self, *args, **options):
        # Roller
        admin_role, _ = Role.objects.get_or_create(name='Admin')
        student_role, _ = Role.objects.get_or_create(name='Student')

        # Admin kullanıcı
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
            )
            admin_user.role = admin_role
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin kullanıcı oluşturuldu: admin / admin123'))
        else:
            self.stdout.write('Admin kullanıcı zaten mevcut (username=admin)')

        # Student kullanıcı
        if not User.objects.filter(username='student').exists():
            student_user = User.objects.create_user(
                username='student',
                email='student@example.com',
                password='student123',
            )
            student_user.role = student_role
            student_user.save()
            self.stdout.write(self.style.SUCCESS('Student kullanıcı oluşturuldu: student / student123'))
        else:
            self.stdout.write('Student kullanıcı zaten mevcut (username=student)')

        self.stdout.write(self.style.SUCCESS('Seed işlemi tamamlandı.'))


