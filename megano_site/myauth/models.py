"""
Модель Профиль пользователей + путь-генерации для аватарки.
"""
from django.contrib.auth.models import User
from django.db import models


def avatar_path(instance: "Avatar", file_name: str) -> str:
    """Директория хранения аватара пользователя"""
    return "users/avatars/{filename}".format(
        filename=file_name,
    )


class Avatar(models.Model):
    """Модель аватара пользователя"""
    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    src = models.ImageField(
        upload_to=avatar_path,
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, default="Аватар", verbose_name="Описание")


class Profile(models.Model):
    """Модель профиля пользователя"""

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    email = models.EmailField(max_length=230, blank=True, null=True, unique=True)
    phone = models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name="Номер телефона")
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
        null=True,
        blank=True
    )
