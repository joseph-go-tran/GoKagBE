from django.apps import apps
from rest_framework import serializers

from authentication.serializers import AuthorSerializer
from questionnaire.models import (InputType, OptionValue, Question,
                                  Questionnaire, SelectType, Statistics, Tags)


class QuestionSummarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    key = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    question_detail = serializers.SerializerMethodField()
    questionnaire = serializers.PrimaryKeyRelatedField(
        queryset=Questionnaire.objects.all()
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "questionnaire",
            "type",
            "key",
            "label",
            "sequence",
            "create_at",
            "question_detail",
        ]

    def get_question_detail(self, obj):
        Model = apps.get_model(app_label="questionnaire", model_name=obj.type)

        if Model is not None:
            related_data = Model.objects.filter(question_key=obj.key)
            serializer_class = globals()[f"{Model.__name__}Serializer"]
            serializer = serializer_class(related_data, many=True)
            return serializer.data[0] if serializer.data else {}


class StatisticViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ["create_at", "views"]


class QuestionnaireSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    questions = QuestionSummarySerializer(many=True, read_only=True)
    statistic_views = StatisticViewsSerializer(many=True, read_only=True)
    likers = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = [
            "id",
            "title",
            "slug",
            "thumb",
            "summary",
            "description",
            "tags",
            "is_collecting",
            "is_public",
            "views",
            "downloads",
            "author",
            "create_at",
            "questions",
            "statistic_views",
            "likers",
        ]

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if not instance.is_public:
    #         newQuestions = [0 for _ in data['questions']]
    #         data['questions'] = newQuestions
    #     return data


class QuestionnaireThumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ["thumb"]


class QuestionnaireLikersSerializer(serializers.ModelSerializer):
    likers = AuthorSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = ["likers"]


class QuestionnaireThumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ["thumb"]


class QuestionSerializer(serializers.ModelSerializer):
    update_by = AuthorSerializer(read_only=True)
    create_by = AuthorSerializer(read_only=True)
    questionnaire = serializers.PrimaryKeyRelatedField(
        queryset=Questionnaire.objects.all()
    )
    id = serializers.IntegerField(read_only=True)
    key = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    question_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "questionnaire",
            "type",
            "key",
            "label",
            "sequence",
            "update_by",
            "update_at",
            "create_by",
            "create_at",
            "question_detail",
        ]

    def get_question_detail(self, obj):
        Model = apps.get_model(app_label="questionnaire", model_name=obj.type)

        if Model is not None:
            related_data = Model.objects.filter(question_key=obj.key)
            serializer_class = globals()[f"{Model.__name__}Serializer"]
            if related_data.count() > 0:
                serializer = serializer_class(related_data.first())
                return serializer.data


class OptionValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OptionValue
        fields = [
            "id",
            "value",
            "create_at",
        ]


class InputTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question_key = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = InputType
        fields = [
            "id",
            "question_key",
            "placeholder",
            "required",
            "create_at",
        ]


class SelectTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question_key = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    options = OptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = SelectType
        fields = [
            "id",
            "question_key",
            "multiselect",
            "html_select",
            "other_field",
            "required",
            "create_at",
            "options",
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        options = self.context.get("options")

        for option in options:
            option["select_type"] = instance
            OptionValue.objects.create(**option)

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        options = self.context.get("options")

        oldOptions = OptionValue.objects.filter(select_type=instance)
        option_ids = [option["id"] for option in options if "id" in option]

        # Remove
        for option in oldOptions:
            if option.id not in option_ids:
                OptionValue.objects.filter(pk=option.id).delete()

        # Update or Create
        for option in options:
            if "id" in option:
                OptionValue.objects.update_or_create(
                    select_type=instance, pk=option["id"], defaults=option
                )
            else:
                option["select_type"] = instance
                OptionValue.objects.create(**option)

        return instance


class TagsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tags
        fields = [
            "id",
            "name",
        ]
