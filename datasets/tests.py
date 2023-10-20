from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from datasets.models import Answer
from questionnaire.models import InputType, Question, Questionnaire


class AnswerViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="testpassword",
        )
        self.questionnaire = Questionnaire.objects.create(
            title="Existing Questionnaire",
            thumb="https://example.com/existing-thumb.jpg",
            tags="tag1|tag4|tag5",
            is_collecting=False,
            is_public=True,
            author=self.user,
        )
        self.question = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Test Question",
            sequence=1,
        )
        InputType.objects.create(
            question_key=self.question.key, placeholder="Enter your anwser"
        )
        self.answer_data = [
            {
                "questionnaire": self.questionnaire.id,
                "question_key": str(self.question.key),
                "value": "Answer 1",
            }
        ]

    def test_create_answer_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/answer/", self.answer_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)

    def test_create_answer_unauthenticated(self):
        response = self.client.post(
            "/api/v1/answer/", self.answer_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)

    def test_create_answer_insufficient_data(self):
        self.client.force_authenticate(user=self.user)
        data = [
            {
                "questionnaire": self.questionnaire.id,
                "question_key": str(self.question.key),
                "value": "Answer 1",
            },
            {
                "questionnaire": self.questionnaire.id,
                "question_key": str(self.question.key),
                "value": "Answer 2",
            },
        ]
        response = self.client.post("/api/v1/answer/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Answer.objects.count(), 0)

    def test_update_answer(self):
        self.client.force_authenticate(user=self.user)
        answer = Answer.objects.create(
            questionnaire=self.questionnaire,
            answer_by=self.user,
            question_key=str(self.question.key),
            value="Initial Value",
        )
        update_data = [{"id": answer.id, "value": "Updated Value 1"}]
        response = self.client.patch(
            "/api/v1/answer/update/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer.refresh_from_db()
        self.assertEqual(answer.value, "Updated Value 1")

    def test_delete_answer(self):
        self.client.force_authenticate(user=self.user)
        answer = Answer.objects.create(
            questionnaire=self.questionnaire,
            answer_by=self.user,
            question_key=str(self.question.key),
            value="To be deleted",
        )
        url = f"/api/v1/answer/{answer.code}/?questionnaire={self.questionnaire.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.filter(id=answer.id).exists(), False)


class DatasetsViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="testpassword",
        )
        self.questionnaire = Questionnaire.objects.create(
            title="Existing Questionnaire",
            thumb="https://example.com/existing-thumb.jpg",
            tags="tag1|tag4|tag5",
            is_collecting=False,
            is_public=True,
            author=self.user,
        )
        self.question = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Test Question",
            sequence=1,
        )
        InputType.objects.create(
            question_key=self.question.key, placeholder="Enter your anwser"
        )
        Answer.objects.create(
            questionnaire=self.questionnaire,
            answer_by=self.user,
            question_key=str(self.question.key),
            value="To be deleted",
        )

    def test_list(self):
        url = "/api/v1/datasets/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        url = "/api/v1/datasets/" + self.questionnaire.slug + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["about"]["title"], self.questionnaire.title
        )
        self.assertEqual(len(response.data["data"]["about"]["questions"]), 1)
