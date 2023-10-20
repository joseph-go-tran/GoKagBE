from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from questionnaire.models import Questionnaire


class IsAuthorQuestionnaireOrReadOnlyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)
        self.questionnaire = Questionnaire.objects.create(
            title="Existing Questionnaire",
            tags="tag1|tag4|tag5",
            is_collecting=False,
            is_public=True,
            author=self.user,
        )
        self.update_data = {
            "title": "Updated Title",
            "summary": "Updated Summary",
            "description": "Updated Description",
        }

    def test_author_can_modify(self):
        response = self.client.patch(
            "/api/v1/questionnaire/" + str(self.questionnaire.id) + "/",
            self.update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_author_cannot_modify(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            "/api/v1/questionnaire/" + str(self.questionnaire.id) + "/",
            self.update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_modify(self):
        other_user = get_user_model().objects.create(
            email="otheruser@example.com",
            password="otherpassword",
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(
            "/api/v1/questionnaire/" + str(self.questionnaire.id) + "/",
            self.update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_only_methods(self):
        other_user = get_user_model().objects.create(
            email="otheruser@example.com",
            password="otherpassword",
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.get(
            "/api/v1/questionnaire/" + str(self.questionnaire.slug) + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            "/api/v1/questionnaire/" + str(self.questionnaire.id) + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
