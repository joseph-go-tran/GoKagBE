# Generated by Django 4.2.3 on 2023-09-28 04:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0011_alter_answer_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"ordering": ["questionnaire", "code"]},
        ),
        migrations.RemoveField(
            model_name="answer",
            name="sequence",
        ),
    ]
