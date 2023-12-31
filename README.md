# Тестовое задание на создание бэкенда для сайта с каталогом книг

## Использованные технологии
- Django
- Django REST Framework
- drf-yasg

## Структура проекта
### Разделение на сервисы (приложения):
- **api**: сервис для API эндпоинтов
- **users**: сервис для работы с пользователями (активация, логин, регистрация)
- **book_catalog**: сервис каталога книг

## Список доступных эндпоинтов:
### Swagger
- */swagger:* документация Swagger
### Приложение users
- */users/csrfCookie:* получение csrf токена
- */users/register:* запрос на регистрацию
- */users/confirm/{user_id}:* запрос на активацию пользователя
- */users/login:* запрос на вход в аккаунт
- */users/authenticated:* запрос на проверку аутентификации
- */users/logout:* запрос на выход из аккаунта
### Приложение api
- */api/book/{book_id}:* получить полную информацию по книге по book_id 
- */api/books:* получить список книг. Доступны необязательные параметры фильтрации:
  - *author_ids:* айди авторов
  - *genre_ids:* айди жанров
  - *from_date:* от даты
  - *to_date:* до даты
  Параметры фильтрации могут быть переданы как в адресе запроса, так и в теле запроса
- */api/addBook:* добавить книгу
- */api/writeReview:* добавить отзыв по книге
- */api/favorite/{book_id}:* добавить в книгу в избранные
- */api/removeFavorite/{book_id}:* удалить книгу из избранных

## Фичи:
- **Регистрация через почту**
- **Отправка ссылки подтверждения на почту. Пример письма:**
<img width="624" alt="image" src="https://github.com/el-bekasto/drf_test_project/assets/57838936/49b26cac-31ab-4a56-a7d6-3de09cb1757f">

- **Ограничение неактивированных пользователей (не могут добавить книгу, отзыв)**
- **Комментарии ко всему коду**
- **Разделение проекта на приложения**
- **Swagger документация**

## Возможные будущие доработки:
- **Добавить перенаправление неактивированных пользователей на страницу с предложением активироваться**
- **Переписать более лаконичные эндпоинты**
- **Добавление Docker/Docker Compose для контейнеризации**
- **Добавление PostgreSQL вместо SQLite и запуск базы так же в Docker**
- **Минимальный фронт на ReactJS**
- **Добавление других видов регистрации через соцсети**
