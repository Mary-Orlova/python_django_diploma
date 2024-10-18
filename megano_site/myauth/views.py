"""
В этом модуле лежат различные представления.
Разные view для пользователей: информация о себе/регистрация/лист пользователей и тд.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Avatar
from .serializers import ProfileSerializer, PasswordSerializer


class SignInView(APIView):
    """Представление аутентификация пользователей/вход"""
    def post(self, request: Request) -> Response:
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """Представление регистрации пользователя"""
    def post(self, request):
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_avatar(request: Request) -> HttpResponse:
    """Представление аватара пользователя"""
    if request.method == "POST":
        avatar = Avatar.objects.create(
            src=request.FILES["avatar"],
            alt=""
        )
        avatar.save()
        profile = Profile.objects.get(user=request.user)
        profile.avatar = avatar
        profile.save()
        return HttpResponse(status=200)


class UpdatePasswordView(APIView):
    """Представление изменения пароля пользователя"""
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request: Request) -> Response:
        self.object = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("currentPassword")):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("newPassword"))
            self.object.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """Представление профиля пользователя, изменение"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, read_only=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        profile = (
            Profile
            .objects
            .get(user=request.user)
        )
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sign_out(request):
    """Представление аватара пользователя"""
    logout(request)
    return Response(status=status.HTTP_200_OK)
