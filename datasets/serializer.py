from rest_framework import serializers

from authentication.serializers import AuthorSerializer
from datasets.models import Answer
from questionnaire.models import Question, Questionnaire


class AnswerSerializer(serializers.ModelSerializer):
    answer_by = AuthorSerializer(read_only=True)
    questionnaire = serializers.PrimaryKeyRelatedField(
        queryset=Questionnaire.objects.all()
    )
    id = serializers.IntegerField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    sequence = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "questionnaire",
            "question_key",
            "value",
            "code",
            "answer_by",
            "create_at",
            "sequence",
        ]

    def get_sequence(self, obj):
        question = Question.objects.filter(key=obj.question_key).first()

        return question.sequence
