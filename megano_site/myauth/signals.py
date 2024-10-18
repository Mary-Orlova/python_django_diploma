"""
Сигналы для создания профилей пользователей и сохранение изменений профилей.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя после регистрации-сигнал"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Сохранение профиля пользователя-сигнал"""
    instance.profile.save()
