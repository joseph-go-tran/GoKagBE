from django.apps import apps
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.exceptions import PermissionDeniedException
from api.mixins import AuthenticationPermissionMixins
from api.permissions import IsAuthorQuestionOrReadOnly
from api.utils import ObjectResponse, StatusResponse
from questionnaire.models import OptionValue, Question
from questionnaire.serializer import (InputTypeSerializer, QuestionSerializer,
                                      SelectTypeSerializer)


class QuestionViewSet(AuthenticationPermissionMixins, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthorQuestionOrReadOnly]

    def create(self, request, *args, **kwargs):
        list_question = []

        # Update "sequence" for all questions gte this new question
        if len(request.data) == 1:
            list_question_gte = Question.objects.filter(
                Q(sequence__gte=request.data[0]["sequence"])
                & Q(questionnaire=request.data[0]["questionnaire"])
            )
            for question in list_question_gte:
                question.sequence += 1
                question.save()

        for question in request.data:
            list_question.append(self.handle_create(request, question))

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Create question successfully!",
                list_question,
            ).get_json(),
            status=status.HTTP_201_CREATED,
        )

    def handle_create(self, request, data, *args, **kwargs):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if (
            serializer.validated_data.get("questionnaire").author
            != request.user
        ):
            raise PermissionDeniedException

        serializer.save(create_by=request.user)

        Model = apps.get_model(
            app_label="questionnaire", model_name=serializer.data.get("type")
        )

        if Model is not None:
            serializer_class = globals()[f"{Model.__name__}Serializer"]
            question_detail = serializer_class(
                data=data.get("question_detail"),
                context={
                    "options": data.get("question_detail")["options"]
                    if "options" in data.get("question_detail")
                    else ""
                },
            )
            question_detail.is_valid(raise_exception=True)
            question_detail.save(question_key=serializer.data.get("key"))

        question_instance = Question.objects.get(id=serializer.data["id"])
        question_serializer = QuestionSerializer(question_instance)

        return question_serializer.data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Update the sequence between the new position and the old position
        if request.data["sequence"] != instance.sequence:
            old_idx = instance.sequence
            new_idx = request.data["sequence"]
            list_question_change = Question.objects.filter(
                Q(sequence__gte=min(old_idx, new_idx))
                & Q(sequence__lte=max(old_idx, new_idx))
                & Q(questionnaire=instance.questionnaire)
                & ~Q(id=instance.id)
            )
            for question in list_question_change:
                question.sequence += (old_idx - new_idx) / abs(
                    old_idx - new_idx
                )
                question.save()

        # Remove old type model
        if request.data["type"] != instance.type:
            Model = apps.get_model(
                app_label="questionnaire", model_name=instance.type
            )

            if Model is not None:
                Model.objects.filter(question_key=instance.key).delete()

            # Create new
            Model = apps.get_model(
                app_label="questionnaire", model_name=request.data["type"]
            )

            if Model is not None:
                serializer_class = globals()[f"{Model.__name__}Serializer"]
                question_detail = serializer_class(
                    data=request.data["question_detail"],
                    context={
                        "options": request.data["question_detail"]["options"]
                        if "options" in request.data["question_detail"]
                        else ""
                    },
                )
                question_detail.is_valid(raise_exception=True)
                question_detail.save(question_key=request.data["key"])

            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            question_updated = serializer.data

        # Update type model
        else:
            instance.update_by = request.user
            question_updated = self.handle_update(instance, request.data)

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Update question successfully!",
                question_updated,
            ).get_json(),
            status=status.HTTP_200_OK,
        )

    def handle_update(self, instance, data, *args, **kwargs):
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        Model = apps.get_model(
            app_label="questionnaire", model_name=instance.type
        )

        if Model is not None:
            question_detail_instance = Model.objects.get(
                question_key=instance.key
            )
            serializer_class = globals()[f"{Model.__name__}Serializer"]
            question_detail = serializer_class(
                question_detail_instance,
                data=data.get("question_detail"),
                partial=True,
                context={
                    "options": data.get("question_detail")["options"]
                    if "options" in data.get("question_detail")
                    else ""
                },
            )
            question_detail.is_valid(raise_exception=True)
            question_detail.save()

        return QuestionSerializer(instance).data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        Model = apps.get_model(
            app_label="questionnaire", model_name=instance.type
        )

        if Model is not None:
            Model.objects.filter(question_key=instance.key).delete()

        list_question_change = Question.objects.filter(
            sequence__gt=instance.sequence
        )
        for question in list_question_change:
            question.sequence -= 1
            question.save()

        instance.delete()

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Delete question successfully!",
                {},
            ).get_json(),
            status=status.HTTP_204_NO_CONTENT,
        )
