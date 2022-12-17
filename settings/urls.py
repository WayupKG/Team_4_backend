from django.contrib import admin
from django.urls import path, include

from .yasg import schema_view

urlpatterns_api_v1 = [
    path('account/', include('apps.account.urls')),
]

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlpatterns_api_v1)),
]

