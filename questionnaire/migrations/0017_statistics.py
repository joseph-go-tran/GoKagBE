# Generated by Django 4.2.3 on 2023-09-19 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0016_questionnaire_downloads"),
    ]

    operations = [
        migrations.CreateModel(
            name="Statistics",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("views", models.IntegerField(default=1)),
                (
                    "questionnaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statistic_views",
                        to="questionnaire.questionnaire",
                    ),
                ),
            ],
            options={
                "db_table": "statistics",
            },
        ),
    ]
