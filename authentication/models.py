from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    password = models.CharField(max_length=200)
    avatar = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        default="https://thumbs.dreamstime.com/b/untitled-213585789.jpg",
    )
    change_password_at = models.DateTimeField(blank=True, null=True)
    go_coin = models.IntegerField(
        validators=[
            MinValueValidator(0, "GoCoin must be greater than or equal to 0!")
        ],
        default=0,
    )
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="user"
    )
    is_staff = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "user"
        ordering = ["create_at"]
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
        ]
        index_together = [
            ("first_name", "last_name"),
            ("last_name", "first_name"),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name + " " + self.last_name)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def change_password(self, new_password):
        self.password = new_password
        self.changePasswordAt = timezone.now()
        self.save()

    @property
    def is_male(self):
        return self.gender == "male"
