import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from authentication.models import User


class Questionnaire(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="questionnaires",
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    thumb = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        default="https://firebasestorage.googleapis.com/v0/b/gokag-19eac.appspot.com/o/defaultQuestionnaire.jpg?alt=media",
    )
    tags = models.CharField(max_length=500, default="DEFAULT")
    summary = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_collecting = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(
        User,
        related_name="likes",
        blank=True,
    )

    class Meta:
        db_table = "questionnaire"
        ordering = ["-create_at"]
        indexes = [
            models.Index(fields=["slug"], name="slug_idx"),
            models.Index(fields=["tags"], name="tags_idx"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        tags = self.tags.split("|")
        for tag_name in tags:
            Tags.objects.get_or_create(name=tag_name.strip())

        super(Questionnaire, self).save(*args, **kwargs)


class Question(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="questions"
    )
    update_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="questions_updated",
    )
    create_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="questions_created",
    )

    type = models.CharField(max_length=50)
    label = models.CharField(max_length=1000)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sequence = models.IntegerField(validators=[MinValueValidator(0)])
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "question"
        ordering = ["questionnaire", "sequence"]
        indexes = [
            models.Index(fields=["questionnaire"], name="questionnaire_idx"),
            models.Index(fields=["sequence"], name="sequence_idx"),
        ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.key = uuid.uuid4()

        super(Question, self).save(*args, **kwargs)


class InputType(models.Model):
    question_key = models.UUIDField(null=False)
    placeholder = models.CharField(max_length=200, null=True, blank=True)
    other_field = models.BooleanField(default=False)
    required = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "input_type"
        ordering = ["create_at"]
        indexes = [
            models.Index(
                fields=["question_key"], name="question_key_inputType_idx"
            ),
        ]


class SelectType(models.Model):
    question_key = models.UUIDField(null=False)
    multiselect = models.BooleanField(default=False)
    html_select = models.BooleanField(default=False)
    other_field = models.BooleanField(default=False)
    required = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "select_type"
        ordering = ["create_at"]
        indexes = [
            models.Index(
                fields=["question_key"], name="question_key_selectType_idx"
            ),
        ]


class OptionValue(models.Model):
    select_type = models.ForeignKey(
        SelectType, on_delete=models.CASCADE, related_name="options"
    )
    value = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "option_value"
        ordering = ["select_type"]
        indexes = [
            models.Index(fields=["select_type"], name="select_type_idx"),
        ]


class Tags(models.Model):
    name = models.CharField(max_length=300, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tags"


class Statistics(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="statistic_views"
    )
    create_at = models.CharField(max_length=100, blank=True, null=True)
    views = models.IntegerField(default=1)

    class Meta:
        db_table = "statistics"
        ordering = ["questionnaire", "create_at"]
        indexes = [
            models.Index(fields=["create_at"], name="create_at_idx"),
        ]

    def save(self, *args, **kwargs):
        current_datetime = timezone.now()

        current_date = current_datetime.date()
        self.create_at = current_date

        super(Statistics, self).save(*args, **kwargs)
