from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, VerifyEmail, LoginAPIView,
                    PasswordTokenCheckAPI, RequestPasswordResetEmail,
                    SetNewPasswordAPIView)

urlpatterns = [
    path('registration', RegisterView.as_view(), name='register'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify'),
    path('login', LoginAPIView.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    path('request-reset-email/',
         RequestPasswordResetEmail.as_view(),
         name='request_reset_email'),

    path('password-reset/<uid64>/<token>/',
         PasswordTokenCheckAPI.as_view(),
         name='password_reset_confirm'),

    path('password-reset-complete',
         SetNewPasswordAPIView.as_view(),
         name='password_reset_complete'),
]
