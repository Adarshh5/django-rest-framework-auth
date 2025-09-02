from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    RegisterAPIView, ActivateAPIView, LoginAPIView,
    PasswordResetRequestAPIView, PasswordResetConfirmAPIView, MeAPIView, LogoutAPIView
)
app_name = "users"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("activate/<str:uidb64>/<str:token>/", ActivateAPIView.as_view(), name="activate"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("password-reset/", PasswordResetRequestAPIView.as_view(), name="password_reset"),
    path("password-reset-confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmAPIView.as_view(), name="password_reset_confirm"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
