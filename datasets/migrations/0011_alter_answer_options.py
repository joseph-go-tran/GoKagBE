# Generated by Django 4.2.3 on 2023-09-28 04:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0010_answer_sequence"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"ordering": ["questionnaire", "code", "sequence"]},
        ),
    ]
