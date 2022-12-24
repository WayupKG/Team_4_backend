from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .yasg import schema_view

from djoser import views as djoser_view

urlpatterns_api_v1 = [
    path('', include('apps.account.urls')),
    path('', include('apps.reception.urls')),
    path('auth/login/', djoser_view.TokenCreateView.as_view(), name='login'),
    path('auth/logout/', djoser_view.TokenDestroyView.as_view(), name='logout'),
]

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlpatterns_api_v1)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

