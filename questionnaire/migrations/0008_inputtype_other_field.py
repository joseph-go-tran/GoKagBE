# Generated by Django 4.2.3 on 2023-08-15 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "questionnaire",
            "0007_selecttype_html_select_selecttype_other_field",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="inputtype",
            name="other_field",
            field=models.BooleanField(default=False),
        ),
    ]
