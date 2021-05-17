from django.urls import path

from authentication.views import (
    RegisterView, LoginAPIView, VerifyEmailView, MyTokenObtainPairView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView
)

app_name = 'users-auth-api'

urlpatterns = [
    path('test/', LoginAPIView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete')
]
