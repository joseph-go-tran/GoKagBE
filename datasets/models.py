from django.db import models

from authentication.models import User
from questionnaire.models import Questionnaire


class Answer(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="answers"
    )
    answer_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="answers"
    )

    question_key = models.UUIDField(null=False)
    value = models.TextField(blank=True, null=True)
    code = models.IntegerField(null=True, default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "answer"
        ordering = ["questionnaire", "code"]
        indexes = [
            models.Index(
                fields=["questionnaire"], name="questionnaire_answer_idx"
            ),
            models.Index(fields=["question_key"], name="question_key_idx"),
            models.Index(fields=["code"], name="code_idx"),
        ]
