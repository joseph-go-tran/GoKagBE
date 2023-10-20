import datetime
import os

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from firebase_admin import storage
from onesignal_sdk.client import Client
from rest_framework import status, viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.exceptions import QuestionnaireIdRequireExcepion, ThumbRequireExcepion
from api.mixins import AuthenticationPermissionMixins
from api.permissions import IsAuthorQuestionnaireOrReadOnly
from api.utils import ObjectResponse, StatusResponse, try_except_wrapper
from questionnaire.models import Questionnaire, Tags
from questionnaire.serializer import (QuestionnaireLikersSerializer,
                                      QuestionnaireSerializer,
                                      QuestionnaireThumbSerializer,
                                      TagsSerializer)


class QuestionnaireViewSet(
    AuthenticationPermissionMixins, viewsets.ModelViewSet
):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthorQuestionnaireOrReadOnly]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Create questionnaire successfully!",
                serializer.data,
            ).get_json(),
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        tags = request.query_params.get("tags") or ""
        key = request.query_params.get("key") or ""
        user_id = request.query_params.get("user_id") or ""
        is_collecting = request.query_params.get("is_collecting") or ""
        min_questions = request.query_params.get("min_questions") or ""
        max_questions = request.query_params.get("max_questions") or ""
        questionnaires = Questionnaire.objects.filter(title__icontains=key)

        if is_collecting:
            questionnaires = questionnaires.filter(is_collecting=is_collecting)

        if user_id:
            questionnaires = questionnaires.filter(author=user_id)

        if tags:
            tag_list = tags.split("|")
            q_objects = Q()
            for tag in tag_list:
                q_objects |= Q(tags__icontains=tag)
            questionnaires = questionnaires.filter(q_objects)

        if min_questions:
            questionnaires = questionnaires.annotate(
                num_questions_count=Count("questions")
            )
            questionnaires = questionnaires.filter(
                num_questions_count__gte=int(min_questions)
            )

        if max_questions:
            questionnaires = questionnaires.annotate(
                num_questions_count=Count("questions")
            )
            questionnaires = questionnaires.filter(
                num_questions_count__lte=int(max_questions)
            )

        page = self.paginate_queryset(questionnaires)
        if page is not None:
            questionnaires_serializer = QuestionnaireSerializer(
                page, many=True
            )
            return self.get_paginated_response(questionnaires_serializer.data)

        questionnaires_serializer = QuestionnaireSerializer(
            questionnaires, many=True
        )

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Get questionnaire successfully!",
                questionnaires_serializer.data,
            ).get_json(),
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        questionnaire_slug = self.kwargs.get("pk")
        questionnaire = get_object_or_404(
            Questionnaire, slug=questionnaire_slug
        )
        questionnaire_serializer = QuestionnaireSerializer(questionnaire)

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Get questionnaire successfully!",
                questionnaire_serializer.data,
            ).get_json(),
            status=status.HTTP_200_OK,
        )

    @action(methods=["PATCH"], url_path="thumb", detail=False)
    @parser_classes([MultiPartParser, FormParser])
    @try_except_wrapper
    def update_thumb(self, request):
        thumb = request.FILES.get("thumb")
        questionnaire = request.query_params.get("questionnaire")

        if thumb is None:
            raise ThumbRequireExcepion
        if questionnaire is None:
            raise QuestionnaireIdRequireExcepion

        filename = (
            str(datetime.datetime.now().timestamp())
            + "."
            + str(thumb.content_type).split("/")[1]
        )
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_string(thumb.read(), content_type=thumb.content_type)

        thumb_url = (
            "https://firebasestorage.googleapis.com/v0/b/gokag-19eac.appspot.com/o/"
            + filename
            + "?alt=media"
        )

        instance = get_object_or_404(Questionnaire, pk=questionnaire)
        questionnaire_serializer = QuestionnaireThumbSerializer(
            instance, data={"thumb": thumb_url}, partial=True
        )
        if questionnaire_serializer.is_valid(raise_exception=True):
            questionnaire_serializer.save()

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Update thumb successfully.",
                questionnaire_serializer.data,
            ).get_json(),
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        url_path="all-tags",
        detail=False,
        permission_classes=[],
        authentication_classes=[],
    )
    @try_except_wrapper
    def get_all_tags(self, request):
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Get all tags successfully.",
                serializer.data,
            ).get_json(),
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["PATCH"],
        url_path="like",
        detail=False,
        permission_classes=[],
    )
    @try_except_wrapper
    def like_datasets(self, request):
        questionnaire_id = request.query_params.get("questionnaire")

        questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
        user = request.user

        if user in questionnaire.likers.all():
            questionnaire.likers.remove(user)
            message = "Questionnaire unliked successfully."
        else:
            one_signal_client = Client(
                app_id=os.getenv("ONE_SIGNAL_APP_ID"),
                rest_api_key=os.getenv("ONE_SIGNAL_REST_API_KEY"),
            )
            print(questionnaire.author.id)
            notification_data = {
                "contents": {"en": user.last_name + " liked your dataset!"},
                "include_external_user_ids": [str(questionnaire.author.id)],
                "data": {
                    "slug": questionnaire.slug,
                },
            }
            one_signal_client.send_notification(notification_data)

            questionnaire.likers.add(user)
            message = "Questionnaire liked successfully."

        # You can also serialize the updated likers field if needed
        serializer = QuestionnaireLikersSerializer(questionnaire)

        return Response(
            {
                "status": "success",
                "message": message,
                "data": serializer.data["likers"],
            },
            status=status.HTTP_200_OK,
        )
