# Generated by Django 4.2.3 on 2023-09-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0019_alter_statistics_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statistics",
            name="create_at",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
