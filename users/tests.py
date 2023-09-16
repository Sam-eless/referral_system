from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


# Create your tests here.
class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(phone="89997770011", email="admin@sky.pro", auth_code=1234, is_staff=True, is_superuser=True)
        self.user.set_password("123131")
        self.user.save()

        response = self.client.post(
            "/users/api/token/",
            {"phone": "89997770011", "password": "123131"},
            format="json"
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_user_create(self):
        response = self.client.post(
            reverse("create_user"),
            {
                "phone": "8908808808",
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.last().phone, "8908808808")
        self.assertEqual(self.user.__str__(), "admin@sky.pro, 89997770011")

    def test_user_auth(self):
        response = self.client.post(
            reverse("auth_user"),
            {
                "phone": "89997770011",
                "auth_code": 1234
            },
            format="json"
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.is_phone_verified, True)

    def test_user_incorrect_auth(self):
        response = self.client.post(
            reverse("auth_user"),
            {
                "phone": "89997770011",
                "auth_code": 9999
            },
            format="json"
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.is_phone_verified, False)

    def test_user_already_auth(self):
        response = self.client.post(
            reverse("auth_user"),
            {
                "phone": "89997770011",
                "auth_code": 1234
            },
            format="json"
        )
        self.user.refresh_from_db()

        response = self.client.post(
            reverse("auth_user"),
            {
                "phone": "89997770011",
                "auth_code": 1234
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.is_phone_verified, True)

    def test_user_does_not_exist_auth(self):
        response = self.client.post(
            reverse("auth_user"),
            {
                "phone": "8903304304",
                "auth_code": 1234
            },
            format="json"
        )
        self.user.refresh_from_db()
        self.assertEqual(response.data, {'error': 'Пользователь с указанным номером не найден'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_list(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        test_user = User.objects.create(phone="8888", auth_code="1111", )
        response = self.client.post(reverse("auth_user"), {"phone": "8888", "auth_code": 1111}, format="json")
        test_user.refresh_from_db()
        valid_data = {
            "received_invite": test_user.self_invite,
        }
        response = self.client.patch(
            reverse('update_user', kwargs={'pk': self.user.id}),
            data=valid_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            reverse('update_user', kwargs={'pk': self.user.id}),
            data=valid_data,
            format="json"
        )
        self.assertEqual(response.data, {'upd error': 'Может быть введен только один инвайт код'})

    def test_user_does_not_exist_update(self):
        valid_data = {
            "received_invite": 1234,
        }
        response = self.client.patch(
            reverse('update_user', kwargs={'pk': self.user.id}),
            data=valid_data,
            format="json"
        )
        self.assertEqual(response.data, {'invite code error': 'Указанный инвайт код не найден'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_detail(self):
        response = self.client.get(reverse('user_detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('user_detail', kwargs={'pk': 1234}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        test_user = User.objects.create(phone="090909", auth_code="1111",)
        response = self.client.post(reverse("auth_user"), {"phone": "8888", "auth_code": 1111}, format="json")
        response = self.client.get(reverse('user_detail', kwargs={'pk': test_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




    def test_user_delete(self):
        response = self.client.delete(
            reverse('delete_user', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
