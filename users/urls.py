from django.urls import path
from .views import *

urlpatterns = [
    # запрос на регистрацию (защищен через csrf)
    path('register/', SignupView.as_view(), name='register'),
    # запрос на получение csrf
    path('csrfCookie/', GetCSRFTokenView.as_view(), name='csrf_cookie'),
    # запрос на вход в аккаунт (защищен через csrf)
    path('login/', LoginView.as_view(), name='login'),
    # запрос на выход из аккаунта (защищен через csrf)
    path('logout/', LogoutView.as_view(), name='logout'),
    # запрос на получение информации о том, вошел пользователь в аккаунт или нет
    path('authenticated/', CheckAuthenticatedView.as_view(), name='checkauth'),
    # запрос на активацию аккаунта
    path('confirm/<int:user_id>', ActivateAccountView.as_view())
]
