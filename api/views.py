from django.shortcuts import render
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from book_catalog.models import *
from book_catalog.serializers import *
from .permissions import IsActivated

from datetime import datetime


class AddBookAPIView(CreateAPIView):
    """
    Представление для обработки запроса на добавление книги
    """
    permission_classes = (IsActivated,)
    serializer_class = CreateBookSerializer


class WriteReviewAPIView(CreateAPIView):
    """
    Представление для обработки запроса на написание отзыва о книге
    """
    permission_classes = (IsActivated,)
    serializer_class = CreateBookReviewSerializer


class GetBookAPIView(APIView):
    """
    Представление для обработки запроса на получение книги по ID
    """
    permission_classes = (AllowAny,)

    def get(self, request, book_id):
        return Response(BookSerializer(Book.objects.get(id=book_id)).data)


class ListBooks(ListAPIView):
    """
    Представление для обработки запроса на список книг. Принимает необязательные параметры фильтрации
    """
    serializer_class = ListBookSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """
        Возвращение queryset для обработки.

        Необязательные параметры в теле запроса и в адресе запроса перечислены ниже:

        - author_ids: Получить книги по айди этих авторов
        - genre_ids: Получить книги по айди этих жанров
        - from_date: Получить книги опубликованные после этой даты (unix timestamp)
        - to_date: Получить книги опубликованные до этой даты (unix timestamp)

        :return: queryset с отфильтрованными книгами по указанным фильтрам
        """
        authors = self.request.query_params.getlist('author_ids') or self.request.data.get('author_ids')
        genres = self.request.query_params.getlist('genre_ids') or self.request.data.get('genre_ids')
        try:
            from_date = datetime.utcfromtimestamp(
                int(self.request.query_params.getlist('from_date') or self.request.data.get('from_date'))
            )
        except TypeError:
            from_date = None
        try:
            to_date = datetime.utcfromtimestamp(
                int(self.request.query_params.getlist('to_date') or self.request.data.get('to_date'))
            )
        except TypeError:
            to_date = None

        qs = Book.objects.all()
        if authors:
            qs = qs.filter(author__in=authors)
        if genres:
            qs = qs.filter(genres__in=genres).distinct()
        if from_date:
            qs = qs.filter(created_at__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__lte=to_date)
        return qs


class GetBooksByRating(ListAPIView):
    """
    Представление для обработки запроса на получение списка книг, отсортированных по рейтингу
    """
    permission_classes = (AllowAny,)
    serializer_class = ListBookSerializer

    def get_queryset(self):
        """
        Отсортировать книги запросом к БД

        :return: queryset с отфильтрованными данными
        """
        return Book.objects.all().annotate(_avg_rating=models.Avg('book_reviews__rating')).order_by('-_avg_rating')
