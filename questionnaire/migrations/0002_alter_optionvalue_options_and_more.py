# Generated by Django 4.2.3 on 2023-08-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="optionvalue",
            options={"ordering": ["select_type"]},
        ),
        migrations.RemoveIndex(
            model_name="optionvalue",
            name="selection_type_idx",
        ),
        migrations.RenameField(
            model_name="optionvalue",
            old_name="selection_type",
            new_name="select_type",
        ),
        migrations.AddIndex(
            model_name="optionvalue",
            index=models.Index(fields=["select_type"], name="select_type_idx"),
        ),
        migrations.AlterModelTable(
            name="selecttype",
            table="select_type",
        ),
    ]
