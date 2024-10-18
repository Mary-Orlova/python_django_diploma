"""
Команды присоедения пользователей в группу.
"""
from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Класс команд для пользователя-добавление разрешений и групп """
    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        group, created = Group.objects.get_or_create(
            name='profile_manager'
        )
        permission_profile = Permission.objects.get(
            codename='view_profile'
        )
        permission_logentry = Permission.objects.get(
            codename='view_logentry',
        )

        #добавление разрешения в группу
        group.permissions.add(permission_profile)

        #связать пользователя напрямую с разрешением
        user.user_permissions.add(permission_logentry)

        #присоединение пользователя к группе
        user.groups.add(group)

        group.save()
        user.save()
