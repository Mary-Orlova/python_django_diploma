"""
Регистрация профиля администратора.
"""
from django.contrib import admin
from .models import Profile, Avatar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "fullName",
        "phone",
        "avatar_id",
        "user_id",
    ]


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'src',
        'alt',
    ]
