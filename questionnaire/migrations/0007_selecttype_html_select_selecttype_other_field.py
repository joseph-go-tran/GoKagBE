# Generated by Django 4.2.3 on 2023-08-15 08:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0006_alter_inputtype_placeholder"),
    ]

    operations = [
        migrations.AddField(
            model_name="selecttype",
            name="html_select",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="selecttype",
            name="other_field",
            field=models.BooleanField(default=False),
        ),
    ]