from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(phone="777").count():
            user = User.objects.create(
                email='admin@sky.pro',
                phone='777',
                first_name='admin',
                last_name='admin',
                is_phone_verified=True,
                is_staff=True,
                is_superuser=True
            )

            user.set_password('123131')
            user.save()
