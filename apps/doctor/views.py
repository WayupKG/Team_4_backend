from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import filters, status, mixins

from.serializers import (
    DoctorSerializer,
    DoctorListSerializer,
    RatingSerializer,
    FeedbackSerializer,
    SpecialtySerializer
)
from .models import Doctor, Specialty, Rating, Feedback


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        if self.action in ['set_rating', 'feedback']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

  
    @action(detail=True, methods=['POST', 'DELETE'])
    def feedback(self, request, pk=None):
        doctor = self.get_object()
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, doctor=doctor)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

    @action(methods=['POST', 'PATCH'], detail=True, url_path='set_rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['doctor'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user=request.user,
            doctor=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method == 'PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Rating object does not exist. Use POST method'})



class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class FeedbackCreateDeleteView(
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
