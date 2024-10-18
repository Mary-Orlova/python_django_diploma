"""Сериализаторы - преобразует информацию, хранящуюся в базе данных и определенную
с помощью моделей Django, в формат, который легко и эффективно передается через API.
Вид (ViewSet): определяет функции (чтение, создание, обновление, удаление), которые будут доступны через API.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара"""
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя"""
    class Meta:
        model = Profile
        fields = [
            "fullName",
            "phone",
            "email",
            "avatar",
        ]

    avatar = AvatarSerializer(read_only=True)


class PasswordSerializer(serializers.ModelSerializer):
    """Сериализатор обновления пароля пользователя"""
    class Meta:
        model = User
        fields = [
            "currentPassword",
            "newPassword",
        ]

    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
