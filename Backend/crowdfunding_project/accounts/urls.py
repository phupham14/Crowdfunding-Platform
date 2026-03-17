# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.wallet import WalletAPIView
from .views.user import RegisterView, EmailLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", EmailLoginView.as_view(), name="user-login"),
    path('wallet/', WalletAPIView.as_view(), name='wallet'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
