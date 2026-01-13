from django.urls import path
from .views import (
    RegisterView, 
    VerifyEmailView, 
    CustomTokenObtainPairView,
    UserProfileView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='activate'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
