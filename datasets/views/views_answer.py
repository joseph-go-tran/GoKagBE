from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.exceptions import AnswerNotEnoughException
from api.utils import ObjectResponse, StatusResponse, try_except_wrapper
from datasets.models import Answer
from datasets.serializer import AnswerSerializer
from questionnaire.models import Question


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = "pk"

    def create(self, request, *args, **kwargs):
        dataset = []

        questions_size = Question.objects.filter(
            questionnaire=request.data[0]["questionnaire"]
        ).count()
        if len(request.data) != questions_size:
            raise AnswerNotEnoughException

        max_code = (
            Answer.objects.filter(
                questionnaire=request.data[0]["questionnaire"]
            )
            .order_by("-code")
            .first()
        )

        for answer in request.data:
            answer["code"] = max_code.code + 1 if max_code is not None else 1
            dataset.append(self.handle_create(request, answer))

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Create answer successfully!",
                dataset,
            ).get_json(),
            status=status.HTTP_201_CREATED,
        )

    def handle_create(self, request, data, *args, **kwargs):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            serializer.save(answer_by=request.user)
        else:
            serializer.save()

        return serializer.data

    @action(
        methods=["PATCH"],
        url_path="update",
        url_name="update-answer",
        detail=False,
    )
    @try_except_wrapper
    def handle_update(self, request, *args, **kwargs):
        dataset = []

        for answer in request.data:
            instance = Answer.objects.get(pk=answer["id"])
            instance.value = answer["value"]
            instance.save()
            serializer = AnswerSerializer(instance)

            dataset.append(serializer.data)

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Update answer successfully!",
                dataset,
            ).get_json(),
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        code = self.kwargs.get("pk")
        questionnaire = request.query_params.get("questionnaire")
        Answer.objects.filter(questionnaire=questionnaire, code=code).delete()

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Delete question successfully!",
                {},
            ).get_json(),
            status=status.HTTP_204_NO_CONTENT,
        )
