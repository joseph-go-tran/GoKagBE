# Generated by Django 4.2.3 on 2023-09-07 03:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0011_alter_questionnaire_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionnaire",
            name="slug",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]