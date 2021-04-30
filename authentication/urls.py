from django.urls import path

from authentication.views import RegisterView, LoginAPIView, VerifyEmailView

app_name = 'users-auth-api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify')
]