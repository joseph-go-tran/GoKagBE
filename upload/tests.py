from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from questionnaire.models import Questionnaire


class UploadViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)
        self.questionnaire = Questionnaire.objects.create(
            title="Existing Questionnaire",
            thumb="https://example.com/existing-thumb.jpg",
            tags="tag1|tag4|tag5",
            is_collecting=False,
            is_public=True,
            author=self.user,
        )

    def test_create_question(self):
        url = "/api/v1/upload/question/"
        data = {
            "file": open("upload/datatests/file.xlsx", "rb"),
            "questionnaire": self.questionnaire.id,
        }
        response = self.client.post(url, data, format="multipart")
        res = self.client.get(
            "/api/v1/datasets/" + self.questionnaire.slug + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["data"]["about"]["questions"]), 1)

    def test_create_datasets(self):
        url = "/api/v1/upload/datasets/"
        data = {
            "file": open("upload/datatests/file.xlsx", "rb"),
            "questionnaire": self.questionnaire.id,
        }
        response = self.client.post(url, data, format="multipart")
        res = self.client.get(
            "/api/v1/datasets/" + self.questionnaire.slug + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["data"]["about"]["questions"]), 1)
        self.assertEqual(len(res.data["data"]["datasets"]), 5)
