"""
Конфигурации приложения myauth и пользователей(использование сигналов).
"""
from django.apps import AppConfig


class MyauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myauth'


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        """
        неявное подключение обработчиков сигналов, использующих @receiver.
        """
        from . import signals


