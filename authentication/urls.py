from django.urls import path

from authentication.views import RegisterView, LoginAPIView, VerifyEmailView, MyTokenObtainPairView

app_name = 'users-auth-api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('test/', LoginAPIView.as_view()),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('login/', MyTokenObtainPairView.as_view(), name='login')
]