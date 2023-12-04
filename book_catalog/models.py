from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User

from datetime import datetime
from typing import List


class BookGenre(models.Model):
    """
    Модель жанра книги

    Attributes:
        name (str): Название жанра
        updated_at (datetime): Дата последнего изменения жанра
        created_at (datetime): Дата создания жанра
    """
    name = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Book genre: {self.name}'


class Book(models.Model):
    """
    Модель книги

    Attributes:
        name (str): Название книги
        author (User): Автор книги
        description (str): Описание книги
        genres (List[BookGenre]): Список жанров книги
        updated_at (datetime): Дата последнего обновления книги
        created_at (datetime): Дата публикации книги
    """
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=5000)
    genres = models.ManyToManyField(BookGenre, related_name='books')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def reviews(self):
        """
        Получить отзывы написанные на данную книгу
        """
        if hasattr(self, '_reviews'):
            return self._reviews
        return self.book_reviews

    @property
    def avg_rating(self):
        """
        Получить среднюю оценку отзывов по книге
        """
        if hasattr(self, '_avg_rating'):
            return self._avg_rating
        return self.book_reviews.aggregate(models.Avg('rating')).values()

    def __str__(self):
        return f'Book: {self.name}'


class BookReview(models.Model):
    """
    Модель отзыва на книгу

    Attributes:
        book (Book): Книга, на которую написан отзыв
        author (User): Автор отзыва
        text (str): Текст отзыва
        rating (int): Оценка отзыва
        updated_at (datetime): Дата последнего изменения отзыва
        created_at (datetime): Дата добавления отзыва
    """
    book = models.ForeignKey(Book, related_name='book_reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000, blank=True)
    rating = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review: {self.text[0:20]}...'
