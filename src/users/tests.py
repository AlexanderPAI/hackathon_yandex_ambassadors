import json

from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User

USER_LOGIN = "user"
USER_EMAIL = "user@ya.ru"
TEST_PASSWORD = "superhardpassword1"
USER_LOGIN_2 = "user2"
USER_EMAIL_2 = "user2@ya.ru"
TEST_PASSWORD_2 = "hardpassword2"


AUTH_URL = "/api/v1/auth/jwt/create"
GET_USER_URL = "/api/v1/auth/users/me/"
GET_USER_ACTIONS = "/api/v1/edit_history/"


class TestCaseWithMockData(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username=USER_LOGIN,
            email=USER_EMAIL,
        )
        self.user.set_password(TEST_PASSWORD)
        self.user.save()
        self.client = APIClient()


class AuthApiTest(TestCaseWithMockData):
    def test_login(self):
        response = self.client.post(
            path=AUTH_URL,
            data=json.dumps({"email": USER_EMAIL, "password": TEST_PASSWORD}),
            content_type="application/json",
        )
        assert response.status_code == 200
        response_dict = response.json()
        assert response_dict.get("access")


class UserApiTest(TestCaseWithMockData):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)

    def test_get_user_obj(self):
        response = self.client.get(
            path=GET_USER_URL.format(pk=self.user.pk),
        )
        assert response.status_code == 200
        data = response.json()
        assert data.keys() == {
            "id",
            "username",
            "email",
        }
        assert data.get("id") == self.user.id

    def test_get_user_actions(self):
        response = self.client.get(
            path=GET_USER_ACTIONS.format(),
        )
        assert response.status_code == 200
