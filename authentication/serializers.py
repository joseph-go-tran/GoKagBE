from rest_framework import serializers

from .models import User


class UserListCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.URLField(read_only=True)
    go_coin = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    role = serializers.CharField(read_only=True)
    is_verify = serializers.BooleanField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "gender",
            "avatar",
            "go_coin",
            "slug",
            "is_active",
            "role",
            "is_verify",
            "create_at",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    go_coin = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_verify = serializers.BooleanField(read_only=True)
    role = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    avatar = serializers.URLField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar",
            "email",
            "slug",
            "gender",
            "go_coin",
            "is_active",
            "role",
            "is_verify",
            "create_at",
        ]


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar"]


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.URLField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
