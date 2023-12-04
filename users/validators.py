from .serializers import *


def validate_register(request_data):
    """
    Валидатор формы регистрации

    :param request_data: тело запроса на регистрацию
    :return: Форма валидна/невалидна
    """
    return RegisterFormSerializer(data=request_data).is_valid()


def validate_login(request_data):
    """
    Валидатор формы входа в аккаунт

    :param request_data: тело запроса на вход
    :return: Форма валидна/невалидна
    """
    return LoginFormSerializer(data=request_data).is_valid()
