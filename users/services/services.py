import string

from datetime import date, timedelta, datetime
import time

from django.utils.crypto import get_random_string

from config import settings
from users.models import User


def set_self_invite():
    return get_random_string(length=6, allowed_chars=string.digits + string.ascii_lowercase + string.ascii_uppercase)


def set_auth_code():
    return get_random_string(length=4, allowed_chars=string.digits)


def reset_auth_code(phone):

    try:
        user = User.objects.get(phone=phone)
        print('пользователь найден')
        # time.sleep(60*60)
        time.sleep(15)
        user.is_phone_verified = False
        user.auth_code = None
        user.set_unusable_password()
        user.save()
    except Exception as error:
        print(error)

