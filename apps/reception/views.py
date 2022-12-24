from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .mixins import ReceptionModelMixin
from .models import Reception
from .serializers import ReceptionSerializer, ReceptionCreateSerializer

from .services.logics import get_receptions

User = get_user_model()


class ReceptionViewSet(ReceptionModelMixin):
    serializer_class = ReceptionSerializer
    queryset = Reception.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return ReceptionCreateSerializer
        return ReceptionSerializer

    @action(detail=False, methods=['GET'], url_path='(?P<user_type>\w+)/(?P<pk>\d+)')
    def receptions(self, request, user_type, pk):
        receptions = get_receptions(user_type, pk)
        if receptions is None:
            return Response('Page not found', status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(receptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

