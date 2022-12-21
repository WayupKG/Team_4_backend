from django.contrib import admin
from django.urls import path, include, re_path

from .yasg import schema_view

from djoser import views as djoser_view

urlpatterns_api_v1 = [
    path('', include('apps.account.urls')),
    path('auth/login/', djoser_view.TokenCreateView.as_view(), name='login'),
    path('auth/logout/', djoser_view.TokenDestroyView.as_view(), name='logout'),
]

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlpatterns_api_v1)),
    path('medizine/', include('apps.doctor.urls')),
]

