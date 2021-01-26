from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer
from lemka_api.utils import Utils
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from lemka.models import User


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user=User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        absurl = 'http://'+current_site+relative_link+'?token='+str(token)
        email_body = 'Bonjour '+user.username+' Cliquez sur le lien suivant pour activer votre compte ... \n'+absurl
        data = { 'email_body': email_body, 'to_email': user.email, 'email_subject': "Vérification d'email" }
        Utils.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    permission_classes = [AllowAny]

    # noinspection PyMethodMayBeStatic
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_201_CREATED)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activtaion Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)