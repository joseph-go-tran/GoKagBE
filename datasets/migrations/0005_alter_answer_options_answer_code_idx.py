# Generated by Django 4.2.3 on 2023-08-11 03:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0004_alter_answer_options_answer_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"ordering": ["questionnaire", "code"]},
        ),
        migrations.AddIndex(
            model_name="answer",
            index=models.Index(fields=["code"], name="code_idx"),
        ),
    ]