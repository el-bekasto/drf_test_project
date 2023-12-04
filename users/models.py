from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime
from uuid import uuid1


class User(AbstractUser):
    """
    Модель пользователя. Наследуется от дефолтной модели Django - AbstractUser

    Attributes:
        username (str): Имя пользователя
        first_name (str): Первое имя пользователя
        last_name (str): Фамилия пользователя
        favorite_books (book_catolog.Book): Избранные книги пользователя
        is_activated (bool): Подтвержденность пользователя
        activation_token (str): Токен для подтверждения регистрации
        updated_at (datetime): Дата последнего изменения данных пользователя
        created_at (datetime): Дата создания пользователя (регистрации)
    """
    favorite_books = models.ManyToManyField('book_catalog.Book', related_name='favorited_users')
    is_activated = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=200, default=uuid1, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'BookCatalogUser {self.username}'
