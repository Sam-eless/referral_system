from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    phone = models.CharField(unique=True, max_length=35, verbose_name='телефон')
    email = models.EmailField(unique=True, verbose_name='почта', **NULLABLE)
    first_name = models.CharField(max_length=100, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name='фамилия', **NULLABLE)
    is_phone_verified = models.BooleanField(verbose_name='телефон подтвержден', default=False)
    auth_code = models.SmallIntegerField(verbose_name='код подтверждения', **NULLABLE)
    self_invite = models.CharField(max_length=6, verbose_name='инвайт код', **NULLABLE)
    # unique = True,
    received_invite = models.ForeignKey('self', on_delete=models.DO_NOTHING, verbose_name='полученный инвайт код', **NULLABLE)
    is_invite_received = models.BooleanField(default=False, verbose_name='введен инвайт код другого пользователя')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('email', 'phone', 'first_name', 'last_name')

    def __str__(self):
        return f'{self.email}, {self.phone}'
