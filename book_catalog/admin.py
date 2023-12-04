from django.contrib import admin
from .models import Book, BookGenre, BookReview

# Регистрация моделей приложения book_catalog в админке
admin.site.register(Book)
admin.site.register(BookGenre)
admin.site.register(BookReview)

