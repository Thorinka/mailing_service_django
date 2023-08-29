from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            last_name='Adminov',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )

        user.set_password('123456')
        user.save()
