# Generated by Django 4.2.3 on 2023-09-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questionnaire", "0008_inputtype_other_field"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="questionnaire",
            name="tag_idx",
        ),
        migrations.RemoveField(
            model_name="questionnaire",
            name="tag",
        ),
        migrations.AddField(
            model_name="questionnaire",
            name="tags",
            field=models.CharField(default="DEFAULT", max_length=500),
        ),
        migrations.AlterField(
            model_name="questionnaire",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="questionnaire",
            name="summary",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="questionnaire",
            name="thumb",
            field=models.URLField(
                blank=True,
                default="https://media.vneconomy.vn/images/upload/2021/04/20/29161-1614162644322449086100.jpg",
                null=True,
            ),
        ),
        migrations.AddIndex(
            model_name="questionnaire",
            index=models.Index(fields=["tags"], name="tags_idx"),
        ),
    ]
