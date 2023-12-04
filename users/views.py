from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import User

from . import validators


@method_decorator(csrf_protect, name='dispatch')
class ActivateAccountView(APIView):
    """
    Представление для обработки запроса на активацию аккаунта
    """
    permission_classes = (AllowAny,)

    def get(self, request: Request, user_id):
        """
        Активация аккаунта. Айди пользователя сравнивается с токеном, который передается в адресе запроса

        :param request: Запрос пользователя
        :param user_id: Айди пользователя, которому нужно активироваться
        :return: Response объект
        """
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'You have to provide token to activate your account!'}, status=401)
        user = User.objects.get(id=user_id)
        if user and not user.is_activated and token == user.activation_token:
            user.is_activated = True
            user.save()
            return Response({'ok': 'You activated your account! Congrats, now you can fully use our service.'}, status=200)
        return Response(
            {
                'error': 'Wrong activation token.'
            },
            status=401
        )



@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    """
    Представление для обработки запроса на регистрацию
    """
    permission_classes = (AllowAny,)

    def post(self, request: Request):
        """
        Обработка запроса на регистрацию. Создание пользователя, который по умолчанию не активирован.
        И отправка на его электронный адрес ссылки для активации.

        :param request: Запрос пользователя
        :return: Response объект
        """
        data = self.request.data

        if not validators.validate_register(data):
            return Response({'details': 'Bad Request Body'}, status=status.HTTP_400_BAD_REQUEST)

        email = data['email']
        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if re_password != password:
            return Response({'error': 'Passwords do not match!'}, status=status.HTTP_401_UNAUTHORIZED)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'This email already registered!'}, status=status.HTTP_409_CONFLICT)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username already exists!'}, status=status.HTTP_409_CONFLICT)
        if len(password) < 8:
            return Response({'erorr': 'Minimum password size is 8 symbols!'}, status=status.HTTP_401_UNAUTHORIZED)

        # Создаем пользователя
        user = User.objects.create_user(email=email, username=username, password=password)

        # Отправляем письмо на адрес пользователя с ссылкой активации
        send_mail(
            subject='Подтверждение вашего аккаунта в DRF TEST PROJECT',
            message=f'Для подтверждения аккаунта сделайте запрос на адрес: /users/confirm/{user.id}?token={user.activation_token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return Response(
            {
                'ok': 'You registered successfully! Now you need to activate your account to fully use our website'
            },
            status=status.HTTP_201_CREATED
        )


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    """
    Представление обработки запроса на вход в аккаунт
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Обработка запроса на вход в аккаунт

        :param request: Запрос пользователя
        :return: Response объект
        """
        data = self.request.data

        if not validators.validate_login(data):
            return Response({'details': 'Bad Request Body'}, status=status.HTTP_400_BAD_REQUEST)

        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'ok': 'You logged in successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Your login or password is incorrect!'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    """
    Представление для обработки запроса на выход из аккаунта
    """
    def post(self, request):
        """
        Обработка запроса на выход из аккаунта

        :param request: Запрос от пользователя
        :return: Response объект
        """
        try:
            logout(request)
            return Response({'ok': 'Logged out!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Something went wrong! {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckAuthenticatedView(APIView):
    """
    Представление для обработки запроса проверки на аутентифицированность (такое слово существует?)
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        """
        Обработка запроса проверки на аутентифицированность (такое слово существует?)

        :param request: Запрос пользователя
        :return: Reponse объект
        """
        if request.user.is_authenticated:
            return Response({'authenticated': True}, status=status.HTTP_200_OK)
        return Response({'authenticated': False}, status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFTokenView(APIView):
    """
    Представление для обработки запроса на получение csrf
    """
    permission_classes = (AllowAny, )

    def get(self, request): # noqa
        """
        Обработка запроса на получение csrf

        :param request: Запрос пользователя
        :return: Response объект
        """
        return Response({'ok': 'CSRF cookie set'})
