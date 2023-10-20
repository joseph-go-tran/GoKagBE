from collections import defaultdict
from operator import itemgetter

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.utils import ObjectResponse, StatusResponse, try_except_wrapper
from datasets.models import Answer
from datasets.serializer import AnswerSerializer
from questionnaire.models import Questionnaire, Statistics
from questionnaire.serializer import QuestionnaireSerializer


class DatasetsViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = "pk"

    @action(
        methods=["GET"],
        url_path="download",
        url_name="download_datasets",
        detail=False,
    )
    @try_except_wrapper
    def download_datasets(self, request):
        questionnaire_slug = request.query_params.get("slug")
        questionnaire = get_object_or_404(
            Questionnaire, slug=questionnaire_slug
        )
        questionnaire_serializer = QuestionnaireSerializer(questionnaire)

        questionnaire.downloads += 1
        questionnaire.save()

        # Get datasets
        datasets = Answer.objects.filter(questionnaire=questionnaire)
        datasets_serializer = AnswerSerializer(datasets, many=True)

        # Group datasets by code
        grouped_datasets = defaultdict(list)
        for dataset in datasets_serializer.data:
            grouped_datasets[dataset["code"]].append(dataset)

        # Sorted datasets by sequence
        results = []
        questions = questionnaire_serializer.data["questions"]
        for code, answers in grouped_datasets.items():
            grouped_datasets_dict = {}
            sorted_answers = sorted(answers, key=itemgetter("sequence"))
            for idx, dataset in enumerate(sorted_answers, start=0):
                grouped_datasets_dict[questions[idx]["label"]] = dataset[
                    "value"
                ]
            results.append(grouped_datasets_dict)

        df = pd.DataFrame(results)

        # Tạo tên tệp XLSX và trả về cho người dùng
        response = HttpResponse(content_type="application/ms-excel")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{questionnaire_slug}.xlsx"'

        # Lưu DataFrame thành tệp Excel (XLSX)
        df.to_excel(response, index=False)

        return response

    def list(self, request, *args, **kwargs):
        return Response(status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        questionnaire_slug = self.kwargs.get("pk")
        questionnaire = get_object_or_404(
            Questionnaire, slug=questionnaire_slug
        )

        questionnaire.views += 1
        questionnaire.save()

        # Statistic views everyday
        current_date = timezone.now().date()

        today_stats = Statistics.objects.filter(
            questionnaire=questionnaire, create_at=current_date
        ).first()

        if today_stats:
            today_stats.views += 1
            today_stats.save()
        else:
            Statistics.objects.create(
                questionnaire=questionnaire, create_at=current_date, views=1
            )

        questionnaire_serializer = QuestionnaireSerializer(questionnaire)

        # Get datasets
        datasets = Answer.objects.filter(questionnaire=questionnaire)
        datasets_serializer = AnswerSerializer(datasets, many=True)

        # Group datasets by code
        grouped_datasets = defaultdict(list)
        for dataset in datasets_serializer.data:
            grouped_datasets[dataset["code"]].append(dataset)

        # Sorted datasets by sequence
        grouped_datasets_dict = {}
        for code, answers in grouped_datasets.items():
            sorted_answers = sorted(answers, key=itemgetter("sequence"))
            grouped_datasets_dict[code] = sorted_answers

        # STATISTICS
        statistic_datasets = []

        for question in questionnaire_serializer.data["questions"]:
            if question["type"] == "InputType":
                obj = {
                    "type": question["type"],
                    "label": question["label"],
                    "statistics": {},
                }
                statistic_datasets.append(obj)
            elif question["type"] == "SelectType":
                statistics = {}
                for option in question["question_detail"]["options"]:
                    statistics[option["value"]] = 0
                obj = {
                    "type": question["type"],
                    "label": question["label"],
                    "multiselect": question["question_detail"]["multiselect"],
                    "statistics": statistics,
                }
                statistic_datasets.append(obj)

        for code in grouped_datasets_dict:
            for idx, answer in enumerate(grouped_datasets_dict[code], start=0):
                if (
                    questionnaire_serializer.data["questions"][idx]["type"]
                    == "InputType"
                ):
                    if (
                        answer["value"]
                        in statistic_datasets[idx]["statistics"]
                    ):
                        statistic_datasets[idx]["statistics"][
                            answer["value"]
                        ] += 1
                    else:
                        # no existed in statistic_datasets
                        statistic_datasets[idx]["statistics"][
                            answer["value"]
                        ] = 1
                elif (
                    questionnaire_serializer.data["questions"][idx]["type"]
                    == "SelectType"
                ):
                    if questionnaire_serializer.data["questions"][idx][
                        "question_detail"
                    ]["multiselect"]:
                        if answer["value"]:
                            answer_split = answer["value"].split(", ")
                            for answer_item in answer_split:
                                if (
                                    answer_item
                                    in statistic_datasets[idx]["statistics"]
                                ):
                                    statistic_datasets[idx]["statistics"][
                                        answer_item
                                    ] += 1
                                else:
                                    pass
                    else:
                        if answer["value"]:
                            if (
                                answer["value"]
                                in statistic_datasets[idx]["statistics"]
                            ):
                                statistic_datasets[idx]["statistics"][
                                    answer["value"]
                                ] += 1
                            else:
                                pass

        response = {
            "about": questionnaire_serializer.data,
            "datasets": grouped_datasets_dict,
            "statistics": statistic_datasets,
        }

        return Response(
            ObjectResponse(
                StatusResponse.STATUS_SUCCESS,
                "Get dataset successfully!",
                response,
            ).get_json(),
            status=status.HTTP_200_OK,
        )
