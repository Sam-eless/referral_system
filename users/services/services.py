import string

from datetime import date, timedelta, datetime

from django.utils.crypto import get_random_string

from config import settings
from users.models import User


def set_self_invite():
    return get_random_string(length=6, allowed_chars=string.digits + string.ascii_lowercase + string.ascii_uppercase)


def set_auth_code():
    return get_random_string(length=4, allowed_chars=string.digits)
