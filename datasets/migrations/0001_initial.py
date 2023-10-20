# Generated by Django 4.2.3 on 2023-08-10 10:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("questionnaire", "0003_alter_question_options_question_sequence_idx"),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_key", models.UUIDField()),
                ("value", models.TextField()),
                ("createAt", models.DateTimeField(auto_now_add=True)),
                (
                    "answerBy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="answers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "questionnaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="answers",
                        to="questionnaire.questionnaire",
                    ),
                ),
            ],
            options={
                "db_table": "answer",
                "ordering": ["question_key"],
                "indexes": [
                    models.Index(
                        fields=["questionnaire"],
                        name="questionnaire_answer_idx",
                    ),
                    models.Index(
                        fields=["question_key"], name="question_key_idx"
                    ),
                ],
            },
        ),
    ]