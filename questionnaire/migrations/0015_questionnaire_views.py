# Generated by Django 4.2.3 on 2023-09-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0014_rename_value_tags_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionnaire",
            name="views",
            field=models.IntegerField(default=0),
        ),
    ]
