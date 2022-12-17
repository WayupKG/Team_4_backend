from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Med Service API",
      default_version='v1',
      description="Система бронирования медицинских услуг",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="help@med-service.online"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
