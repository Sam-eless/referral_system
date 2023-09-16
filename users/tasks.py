from celery import shared_task

from users.models import User
from users.services.services import reset_auth_code


@shared_task
def shared_reset_auth_code(user: User):
    reset_auth_code(user)

