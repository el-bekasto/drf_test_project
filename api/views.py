from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status

from api.serializers import *

from datetime import datetime


class RemoveBookFromFavorites(APIView):
    """
    Представление для удаления книги из избранных
    """
    def get(self, request: Request, book_id):
        """
        Удаляет книгу из избранных, если такая книга существует и находится в избранных. Иначе возвращает ошибку
        :param request: Запрос пользователя
        :param book_id: Айди книги, которую нужно удалить
        :return: Response объект
        """
        if not Book.objects.filter(id=book_id).exists():
            return Response({'error': 'Book does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        if not User.objects.filter(favorite_books__id=book_id).exists():
            return Response({'error': 'This book is not in your favorites!'}, status=status.HTTP_409_CONFLICT)
        request.user.favorite_books.remove(Book.objects.get(id=book_id))
        request.user.save()
        return Response({'ok': 'You removed this book from your favorites'})


class AddBookToFavorite(APIView):
    """
    Представление для добавления книги в избранные
    """
    def get(self, request: Request, book_id):
        """
        Добавляет книгу в избранные, если она существует и не находится в избранных

        :param request: Запрос пользователя
        :param book_id: Айди книги, которую нужно добавить
        :return: Response объект
        """
        if not Book.objects.filter(id=book_id).exists():
            return Response({'error': 'Book does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        if User.objects.filter(favorite_books__id=book_id).exists():
            return Response({'error': 'You already added this book to your favorites!'}, status=status.HTTP_409_CONFLICT)
        request.user.favorite_books.add(Book.objects.get(id=book_id))
        request.user.save()
        return Response({'ok': f'You added book (id={book_id}) to your favorites!'}, status=status.HTTP_200_OK)


class AddBookAPIView(CreateAPIView):
    """
    Представление для обработки запроса на добавление книги
    """
    serializer_class = CreateBookSerializer


class WriteReviewAPIView(CreateAPIView):
    """
    Представление для обработки запроса на написание отзыва о книге
    """
    serializer_class = CreateBookReviewSerializer


class GetBookAPIView(APIView):
    """
    Представление для обработки запроса на получение книги по ID
    """
    permission_classes = (AllowAny,)

    def get(self, request, book_id):
        return Response(BookSerializer(Book.objects.get(id=book_id), context={'request': request}).data)


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
