"""Разрешения-доступ для пользователя"""
from rest_framework import permissions


class OrderOwner(permissions.BasePermission):
    """Проверка доступа - что владелец заказа или администратор"""
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.user == request.user or request.user.is_admin
