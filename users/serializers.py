from rest_framework import serializers


class LoginFormSerializer(serializers.Serializer): # noqa
    """
    Сериализатор для валидации формы входа в аккаунт

    Attributes:
        username (str): Имя пользователя
        password (str): Пароль пользователя
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RegisterFormSerializer(serializers.Serializer): # noqa
    """
    Сериализатор для валидации формы регистрации

    Attributes:
        email (str): Электронный адрес пользователя
        username (str): Имя пользователя
        password (str): Пароль пользователя
        re_password (str): Повторение пароля для подтверждения
    """
    email = serializers.EmailField()
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, min_length=8)
    re_password = serializers.CharField(required=True)
