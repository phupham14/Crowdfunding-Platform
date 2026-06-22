# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.project_owner_application import (
    MyProjectOwnerApplicationAPIView,
    ProjectOwnerApplicationApproveAPIView,
    ProjectOwnerApplicationListAPIView,
    ProjectOwnerApplicationRejectAPIView,
)
from .views.user import EmailLoginView, RegisterView
from .views.wallet import WalletAPIView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", EmailLoginView.as_view(), name="user-login"),
    path("wallet/", WalletAPIView.as_view(), name="wallet"),
    path(
        "project-owner-applications/me/",
        MyProjectOwnerApplicationAPIView.as_view(),
        name="my-project-owner-application",
    ),
    path(
        "project-owner-applications/",
        ProjectOwnerApplicationListAPIView.as_view(),
        name="project-owner-application-list",
    ),
    path(
        "project-owner-applications/<int:pk>/approve/",
        ProjectOwnerApplicationApproveAPIView.as_view(),
        name="project-owner-application-approve",
    ),
    path(
        "project-owner-applications/<int:pk>/reject/",
        ProjectOwnerApplicationRejectAPIView.as_view(),
        name="project-owner-application-reject",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
