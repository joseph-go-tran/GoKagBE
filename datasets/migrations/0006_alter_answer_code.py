# Generated by Django 4.2.3 on 2023-08-11 03:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0005_alter_answer_options_answer_code_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="code",
            field=models.IntegerField(null=True),
        ),
    ]
