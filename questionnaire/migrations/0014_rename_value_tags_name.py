# Generated by Django 4.2.3 on 2023-09-07 07:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0013_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tags",
            old_name="value",
            new_name="name",
        ),
    ]
