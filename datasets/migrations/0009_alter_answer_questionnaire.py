# Generated by Django 4.2.3 on 2023-09-28 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0023_alter_questionnaire_thumb"),
        ("datasets", "0008_alter_answer_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="questionnaire",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="questionnaire.questionnaire",
            ),
        ),
    ]
