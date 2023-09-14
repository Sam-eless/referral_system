from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from users.models import User


class ReceivedInviteValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(value.get("received_invite"))
        invited_user = value.get("received_invite")
        print(invited_user.self_invite)
        if value.get("received_invite") is not None:
            received_invite = invited_user.self_invite
            try:
                user = User.objects.get(self_invite=received_invite)
                if user.is_invite_received:
                    raise serializers.ValidationError("Может быть введен только один инвайт код")
                else:
                    user.is_invite_received = True
                    user.save()
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Указанный инвайт код не найден")

