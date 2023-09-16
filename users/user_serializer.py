from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    received_invite = SlugRelatedField(slug_field='self_invite', queryset=User.objects.all())
    invited_users = serializers.SerializerMethodField()

    def to_representation(self, instance):
        result = super(UserSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    def get_invited_users(self, obj: User) -> list:
        queryset = User.objects.filter(received_invite=obj)
        if len(queryset) == 0:
            return None
        else:
            return [UserPhoneSerializer(q).data for q in queryset]

    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name", "self_invite", "received_invite", "invited_users"]


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']


class UserListSerializer(serializers.ModelSerializer):
    received_invite = SlugRelatedField(slug_field='self_invite', queryset=User.objects.all())
    invited_users = serializers.SerializerMethodField()

    def to_representation(self, instance):
        result = super(UserListSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    def get_invited_users(self, obj):
        queryset = User.objects.filter(received_invite=obj)
        if len(queryset) == 0:
            return None
        else:
            return [UserPhoneSerializer(q).data for q in queryset]

    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name", "self_invite", "received_invite", "invited_users"]


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "auth_code", "is_phone_verified"]


class UserCreateSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["phone"]
