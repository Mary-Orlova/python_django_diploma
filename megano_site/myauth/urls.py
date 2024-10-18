"""
Подключения для различных представлений приложения myauth.
"""

from django.urls import path
from .views import (
    SignInView,
    SignUpView,
    sign_out,
    ProfileView,
    UpdatePasswordView,
    update_avatar,
    )

app_name = "myauth"

urlpatterns = [
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="register"),
    path("sign-out", sign_out, name="sign_out"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/avatar", update_avatar, name="update_avatar"),
    path("profile/password", UpdatePasswordView.as_view(), name="update_password"),
]


