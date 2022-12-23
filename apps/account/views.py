from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .mixins import UserMixinSet, DoctorMixinSet
from .models import Specialty, Feedback
from .services import constants as cns
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    PasswordChangeSerializer,
    RestorePasswordSerializer,
    SetRestorePasswordSerializer, SpecialtySerializer, FeedbackSerializer, DoctorSerializer
)

User = get_user_model()


class UserViewSet(UserMixinSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(user_type=cns.USER)
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


class DoctorViewSet(DoctorMixinSet):
    queryset = User.objects.filter(user_type=cns.DOCTOR)
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        if self.action in ['feedbacks']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['feedbacks']:
            return FeedbackSerializer
        return DoctorSerializer

    @action(detail=True, methods=['GET', 'POST'])
    def feedbacks(self, request, pk=None):
        doctor = self.get_object()
        if request.POST:
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.request.user, doctor=doctor)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        feedbacks = Feedback.objects.filter(doctor=doctor)
        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialtyViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

