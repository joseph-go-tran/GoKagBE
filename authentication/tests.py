from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "tranduykhuongit@gmail.com",
            "password": "testpassword",
            "gender": "male",
            "role": "user",
        }
        self.login_data = {
            "email": "tranduykhuongit@gmail.com",
            "password": "testpassword",
        }
        self.login_url = "/api/v1/auth/login/"
        self.register_url = "/api/v1/auth/register/"
        self.logout_url = "/api/v1/auth/logout/"
        self.profile_url = "/api/v1/auth/profile/"
        self.update_url = "/api/v1/auth/update/"
        self.avatar_url = "/api/v1/auth/avatar/"

    def test_user_registration(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_no_email(self):
        response = self.client.post(
            self.register_url, {**self.user_data, "email": ""}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_no_password(self):
        response = self.client.post(
            self.register_url,
            {**self.user_data, "password": ""},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        response = self.client.post(
            self.login_url, self.login_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url, self.login_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_failed(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(
            self.login_url,
            {**self.login_data, "password": "123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        # Log in user first
        self.client.post(self.register_url, self.user_data, format="json")
        user = self.client.post(self.login_url, self.login_data, format="json")
        response = self.client.post(
            self.logout_url,
            {"refresh_token": user.data["data"]["refresh_token"]},
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {user.data["data"]["access_token"]}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout_no_token(self):
        # Log in user first
        self.client.post(self.register_url, self.user_data, format="json")
        user = self.client.post(self.login_url, self.login_data, format="json")

        response = self.client.post(
            self.logout_url,
            {"refresh_token": user.data["data"]["refresh_token"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout_no_login(self):
        # Log in user first
        self.client.post(self.register_url, self.user_data, format="json")
        user = self.client.post(self.login_url, self.login_data, format="json")
        response = self.client.post(
            self.logout_url,
            {"refresh_token": user.data["data"]["refresh_token"]},
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {user.data["data"]["access_token"]}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.logout_url,
            {"refresh_token": user.data["data"]["refresh_token"]},
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {user.data["data"]["access_token"]}',
        )
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_user_profile(self):
        self.client.post(self.register_url, self.user_data, format="json")
        user = self.client.post(self.login_url, self.login_data, format="json")
        response = self.client.get(
            self.profile_url,
            HTTP_AUTHORIZATION=f'Bearer {user.data["data"]["access_token"]}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_profile(self):
        self.client.post(self.register_url, self.user_data, format="json")
        user = self.client.post(self.login_url, self.login_data, format="json")
        updated_data = {"first_name": "Updated First Name"}
        response = self.client.patch(
            self.update_url,
            updated_data,
            format="json",
            HTTP_AUTHORIZATION=f'Bearer {user.data["data"]["access_token"]}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["first_name"], updated_data["first_name"]
        )
