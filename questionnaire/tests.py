from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import InputType, OptionValue, Question, Questionnaire, SelectType


class QuestionnaireViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)
        self.questionnaire_data = {
            "title": "Test Questionnaire",
            "tags": "tag1|tag2|tag3",
            "is_collecting": True,
            "is_public": True,
        }
        self.questionnaire = Questionnaire.objects.create(
            title="Existing Questionnaire",
            thumb="https://example.com/existing-thumb.jpg",
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
        self.create_url = "/api/v1/questionnaire/"

    def test_create_questionnaire_success(self):
        response = self.client.post(
            self.create_url, self.questionnaire_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_questionnaire_invalid_data(self):
        invalid_data = {
            "title": "",
            "summary": "Summary",
            "description": "Description",
        }
        response = self.client.post(
            self.create_url, invalid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_questionnaire_check_database(self):
        response = self.client.post(
            self.create_url, self.questionnaire_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that questionnaire has been created successfully
        created_questionnaire = Questionnaire.objects.filter(
            title=self.questionnaire_data["title"]
        ).first()
        self.assertIsNotNone(created_questionnaire)

        # Check that data has been created correctly
        self.assertEqual(created_questionnaire.author, self.user)
        self.assertEqual(
            created_questionnaire.title, self.questionnaire_data["title"]
        )

    def test_list_questionnaires(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_questionnaire(self):
        retrieve_url = f"{self.create_url}{self.questionnaire.slug}/"
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_questionnaire(self):
        response = self.client.patch(
            self.create_url + str(self.questionnaire.id) + "/",
            self.update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.questionnaire.refresh_from_db()
        self.assertEqual(self.questionnaire.title, self.update_data["title"])
        self.assertEqual(
            self.questionnaire.summary, self.update_data["summary"]
        )
        self.assertEqual(
            self.questionnaire.description, self.update_data["description"]
        )

    def test_update_questionnaire_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            self.create_url + str(self.questionnaire.id) + "/",
            self.update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_questionnaire_non_author(self):
        # Create another user
        other_user = get_user_model().objects.create(
            email="otheruser@example.com",
            password="otherpassword",
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(
            self.create_url + str(self.questionnaire.id) + "/",
            self.update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_questionnaire(self):
        response = self.client.delete(
            self.create_url + str(self.questionnaire.id) + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Questionnaire.objects.filter(pk=self.questionnaire.pk).exists()
        )

    def test_delete_questionnaire_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            self.create_url + str(self.questionnaire.id) + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_questionnaire_non_author(self):
        other_user = get_user_model().objects.create(
            email="otheruser@example.com",
            password="otherpassword",
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(
            self.create_url + str(self.questionnaire.id) + "/"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class QuestionViewSetTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
            password="testpassword",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.questionnaire = Questionnaire.objects.create(
            author=self.user,
            title="Test Questionnaire",
            slug="test-questionnaire",
        )

    def test_create_question(self):
        data = [
            {
                "questionnaire": self.questionnaire.id,
                "type": "InputType",
                "label": "Test Input Question",
                "sequence": 1,
                "question_detail": {
                    "placeholder": "Enter your anwser",
                    "other_field": True,
                    "required": True,
                },
            }
        ]

        response = self.client.post("/api/v1/question/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(OptionValue.objects.count(), 0)

    def test_create_select_question_with_options(self):
        data = [
            {
                "questionnaire": self.questionnaire.id,
                "type": "SelectType",
                "label": "Test Select Question",
                "sequence": 1,
                "question_detail": {
                    "multiselect": True,
                    "html_select": False,
                    "options": [
                        {"value": "Option 1"},
                        {"value": "Option 2"},
                        {"value": "Option 3"},
                    ],
                },
            }
        ]

        response = self.client.post("/api/v1/question/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        question = Question.objects.first()
        self.assertEqual(question.type, "SelectType")
        self.assertEqual(question.label, "Test Select Question")

        select_type = SelectType.objects.get(question_key=question.key)
        self.assertTrue(select_type.multiselect)
        self.assertFalse(select_type.html_select)
        self.assertEqual(select_type.options.count(), 3)

    def test_update_question(self):
        data = [
            {
                "questionnaire": self.questionnaire.id,
                "type": "InputType",
                "label": "Test Input Question",
                "sequence": 1,
                "question_detail": {
                    "placeholder": "Enter your anwser",
                    "other_field": True,
                    "required": True,
                },
            }
        ]

        question = self.client.post("/api/v1/question/", data, format="json")

        data = {
            "type": "InputType",
            "label": "Updated Input Question",
            "sequence": 2,
            "question_detail": {
                "placeholder": "Updated placeholder",
                "required": False,
            },
        }
        response = self.client.patch(
            f"/api/v1/question/{question.data['data'][0]['id']}/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question_sequence(self):
        question1 = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Question 1",
            sequence=1,
        )
        question2 = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Question 2",
            sequence=2,
        )

        InputType.objects.create(
            question_key=question2.key, placeholder="Enter your anwser"
        )

        data = {"type": "InputType", "sequence": 1, "question_detail": {}}

        response = self.client.patch(
            f"/api/v1/question/{question2.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        question1.refresh_from_db()
        question2.refresh_from_db()
        self.assertEqual(question1.sequence, 2)
        self.assertEqual(question2.sequence, 1)

    def test_update_question_type_and_detail(self):
        question = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Test Input Question",
            sequence=1,
        )

        InputType.objects.create(
            question_key=question.key, placeholder="Enter your answer"
        )

        data = {
            "key": question.key,
            "type": "SelectType",
            "label": "Updated Select Question",
            "sequence": 2,
            "question_detail": {
                "multiselect": True,
                "html_select": True,
                "options": [
                    {"value": "Option 1"},
                    {"value": "Option 2"},
                    {"value": "Option 3"},
                ],
            },
        }

        response = self.client.patch(
            f"/api/v1/question/{question.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        question.refresh_from_db()
        self.assertEqual(question.type, "SelectType")

        select_type = SelectType.objects.get(question_key=question.key)
        self.assertTrue(select_type.multiselect)
        self.assertTrue(select_type.html_select)
        self.assertEqual(select_type.options.count(), 3)

    def test_update_question_detail_only(self):
        question = Question.objects.create(
            questionnaire=self.questionnaire,
            type="SelectType",
            label="Test Select Question",
            sequence=1,
        )

        options = [{"value": "Option 1"}, {"value": "Option 2"}]

        SelectType.objects.create(
            question_key=question.key, multiselect=True, html_select=False
        )

        data = {
            "key": question.key,
            "type": "SelectType",
            "label": "Updated Select Question",
            "sequence": 2,
            "question_detail": {
                "multiselect": False,
                "html_select": True,
                "options": options,
            },
        }

        response = self.client.patch(
            f"/api/v1/question/{question.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        question.refresh_from_db()

        select_type = SelectType.objects.get(question_key=question.key)
        self.assertFalse(select_type.multiselect)
        self.assertTrue(select_type.html_select)
        self.assertEqual(select_type.options.count(), 2)

    def test_delete_question(self):
        question = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Test Input Question",
            sequence=1,
        )

        response = self.client.delete(f"/api/v1/question/{question.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

    def test_delete_question_should_delete_input_type(self):
        question = Question.objects.create(
            questionnaire=self.questionnaire,
            type="InputType",
            label="Test Input Question",
            sequence=1,
        )

        InputType.objects.create(
            question_key=question.key, placeholder="Enter your answer"
        )

        response = self.client.delete(f"/api/v1/question/{question.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        input_type_count = InputType.objects.filter(
            question_key=question.key
        ).count()
        self.assertEqual(input_type_count, 0)
