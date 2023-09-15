import time
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from users.models import User
from users.services.services import set_self_invite, set_auth_code
from users.user_serializer import UserSerializer, UserCreateSerializer, UserAuthSerializer, UserListSerializer, \
    UserPhoneSerializer


# Create your views here.
class UserCreateView(CreateAPIView):
    serializer_class = UserPhoneSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(responses={200: UserSerializer()})
    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        try:
            user_auth_code = set_auth_code()
            user = User.objects.create(
                phone=phone,
                auth_code=user_auth_code,
                # ОБНУЛЯТЬ КОД ЧЕРЕЗ ЧАС
            )
            user.set_password(user_auth_code)
            user.save()
            time.sleep(3)
            print(user.auth_code)
            return Response({'auth': "На ваш номер отправлен код подтверждения, введите auth_code"},
                            status=status.HTTP_200_OK)
        except Exception as error:
            time.sleep(3)
            return Response({'auth': "На ваш номер отправлен код подтверждения, введите auth_code"},
                            status=status.HTTP_200_OK)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthUpdateView(UpdateAPIView):
    serializer_class = UserAuthSerializer
    queryset = User.objects.all()

    # permission_classes = [IsAuthenticated, OwnerOrStuff]
    @swagger_auto_schema(responses={200: UserAuthSerializer()})
    def post(self, request, *args, **kwargs):
        try:
            phone = request.data['phone']
            try:
                user = User.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return Response({'error': "Пользователь с указанным номером не найден"},
                                status=status.HTTP_400_BAD_REQUEST)
            if user.is_phone_verified:
                return Response({'auth error': "Пользователь уже авторизован"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if user.auth_code == request.data['auth_code']:
                    user.is_phone_verified = True
                    user.self_invite = set_self_invite()
                    user.save()
                    request.data['is_phone_verified'] = user.is_phone_verified
                    #     СНИМАТЬ ФЛАЖОК ЧЕРЕЗ СУТКИ
                else:
                    return Response({'auth error': "Неверный код авторизации"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(request.data, status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated, OwnerOrStuff]


class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated, OwnerOrStuff]
    # pagination_class = CustomPagination


class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = [IsAuthenticated, OwnerOrStuff]
    @swagger_auto_schema(responses={200: UserSerializer()})
    def partial_update(self, request, *args, **kwargs):
        if request.data["received_invite"]:
            try:
                if self.kwargs["pk"]:
                    user = User.objects.get(pk=self.kwargs["pk"])
                    invited_user = request.data["received_invite"]
                    user.received_invite = User.objects.get(self_invite=invited_user)
                    if user.is_invite_received:
                        raise serializers.ValidationError("Может быть введен только один инвайт код")
                    else:
                        user.is_invite_received = True
                        print(user.received_invite)
                    user.save()
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Указанный инвайт код не найден")

        return super().partial_update(request, *args, **kwargs)
