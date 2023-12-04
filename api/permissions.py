from rest_framework import permissions


class IsActivated(permissions.BasePermission):
    """
    Кастомное разрешение для определения активирован пользователь или нет.
    """
    def has_permission(self, request, view):
        """
        Проверка активированности пользователя с помощью объекта request.user

        :param request: Запрос пользователя
        :param view: Представление
        :return: Определение активированности пользователя
        """
        return bool(request.user.is_authenticated and request.user.is_activated)
