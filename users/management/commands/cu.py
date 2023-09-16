from django.core.management import BaseCommand

from users.models import User
from users.services.services import set_self_invite


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(phone="111").count():
            user = User.objects.create(
                email='test1@sky.pro',
                phone='111',
                first_name='test1',
                last_name='test1',
                is_staff=False,
                is_superuser=False,
                self_invite=set_self_invite()
            )

            user.set_password('123')
            user.save()
        if not User.objects.filter(phone="222").count():
            user = User.objects.create(
                email='test2@sky.pro',
                phone='222',
                first_name='test2',
                last_name='test2',
                is_staff=False,
                is_superuser=False,
                self_invite=set_self_invite()

            )

            user.set_password('123')
            user.save()
        if not User.objects.filter(phone="333").count():
            user = User.objects.create(
                email='test3@sky.pro',
                phone='333',
                first_name='test3',
                last_name='test3',
                is_staff=False,
                is_superuser=False,
                self_invite=set_self_invite()
            )

            user.set_password('123')
            user.save()
