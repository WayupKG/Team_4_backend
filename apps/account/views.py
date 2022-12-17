from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from .mixins import UserMixinSet

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    PasswordChangeSerializer,
    RestorePasswordSerializer,
    SetRestorePasswordSerializer
)

User = get_user_model()


class UserViewSet(UserMixinSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    token_generator = default_token_generator

    @action(["post"], detail=False, serializer_class=UserRegistrationSerializer)
    def registration(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Thanks for registration. Activate your account via link in your mail',
                status=status.HTTP_201_CREATED
            )

    @action(["post"], detail=False,
            serializer_class=PasswordChangeSerializer,
            permission_classes=[IsAuthenticated])
    def password_change(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Password changed succesfully',
                status=status.HTTP_200_OK
            )

    @action(["post"], detail=False, serializer_class=RestorePasswordSerializer)
    def password_restore(self, request, *args, **kwargs):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Code was sent to your email',
                status=status.HTTP_200_OK
            )

    @action(["post"], detail=False, serializer_class=SetRestorePasswordSerializer)
    def password_set_restored(self, request, *args, **kwargs):
        serializer = SetRestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Password restored successfully',
                status=status.HTTP_200_OK
            )

