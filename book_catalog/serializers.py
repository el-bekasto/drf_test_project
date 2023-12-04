from rest_framework.serializers import HiddenField, CurrentUserDefault, ModelSerializer, ReadOnlyField, SerializerMethodField
from .models import *

from typing import List


class BookReviewSerializer(ModelSerializer):
    """
    Сериализатор отзывов на книгу
    """

    class Meta:
        """
        Метаданные о классе-сериализаторе

        Attributes:
            model (object): Модель, которую сериализирует сериализатор
            fields (List[str]): Список полей модели для сериализации
        """
        model = BookReview
        fields = ['id', 'book', 'author', 'text', 'rating']


class CreateBookReviewSerializer(ModelSerializer):
    """
    Сериализатор создания отзывов на книгу

    Attributes:
        author (HiddenField): Автор отзыва, текущий пользователь, от которого запрос
    """
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        """
        Метаданные о классе-сериализаторе

        Attributes:
            model (object): Модель, которую сериализирует сериализатор
            fields (List[str]): Список полей модели для сериализации
        """
        model = BookReview
        fields = ['id', 'book', 'author', 'text', 'rating']


class ListBookSerializer(ModelSerializer):
    """
    Сериализатор для списка книг

    Attributes:
        avg_rating (ReadOnlyField): средний рейтинг книги по отзывам
    """
    avg_rating = ReadOnlyField()

    class Meta:
        """
        Метаданные о классе-сериализаторе

        Attributes:
            model (object): Модель, которую сериализирует сериализатор
            fields (List[str]): Список полей модели для сериализации
        """
        model = Book
        fields = ['id', 'name', 'genres', 'author', 'avg_rating']


class BookSerializer(ListBookSerializer):
    """
    Сериализатор для книг

    Attributes:
        reviews (SerializerMethodField): Отзывы на книгу
    """
    reviews = SerializerMethodField()

    def get_reviews(self, obj):
        """
        Вернуть сериализированный список отзывов на книгу

        :param obj: Объект книги
        :return: Сериализированный JSON-список отызвов на книгу
        """
        return BookReviewSerializer(obj.book_reviews, many=True).data

    class Meta(ListBookSerializer.Meta):
        """
        Метаданные о классе-сериализаторе

        Attributes:
            model (object): Модель, которую сериализирует сериализатор
            fields (List[str]): Список полей модели для сериализации
        """
        model = Book
        fields = ListBookSerializer.Meta.fields + ['description', 'created_at', 'reviews']


class CreateBookSerializer(ModelSerializer):
    """
    Сериализатор для публикации книги

    Attributes:
        author (HiddenField): Автор книги, пользователь от которого идет запрос
    """
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        """
        Метаданные о классе-сериализаторе

        Attributes:
            model (object): Модель, которую сериализирует сериализатор
            fields (List[str]): Список полей модели для сериализации
        """
        model = Book
        fields = ['name', 'author', 'description', 'genres']
