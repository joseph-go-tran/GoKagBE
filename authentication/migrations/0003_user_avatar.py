# Generated by Django 4.2.3 on 2023-08-02 04:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_alter_user_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.URLField(blank=True, null=True),
        ),
    ]