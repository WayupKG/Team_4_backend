from django.urls import path
from .views import (
    RegistrationView, 
    AccountActivationView,
    ChangePasswordView,
    RestorePasswordView,
    SetRestoredPasswordView,
    DeleteAccountView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<str:activation_code>/', AccountActivationView.as_view(), name='activation'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('password/restore/', RestorePasswordView.as_view(), name='restore_password'),
    path('password/set-restored/', SetRestoredPasswordView.as_view(), name='set_restored_password'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account')
]


