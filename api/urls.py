from django.urls import path

from .views import *

urlpatterns = [
    # запрос на получение конкретной книги по ID
    path('book/<int:book_id>', GetBookAPIView.as_view()),
    # запрос на получение списка книг, с необязательной фильтрацией
    path('books/', ListBooks.as_view()),
    # запрос на добавление книги (только зарегистрированные пользователи)
    path('addBook/', AddBookAPIView.as_view()),
    # запрос на написание отзыва о книге (только зарегистрированные пользователи)
    path('writeReview/', WriteReviewAPIView.as_view()),
    # запрос на добавление книги в избранные
    path('favorite/<int:book_id>', AddBookToFavorite.as_view()),
    # запрос на удаление книги из избранных
    path('removeFavorite/<int:book_id>', RemoveBookFromFavorites.as_view())
]
