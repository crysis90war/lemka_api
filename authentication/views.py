import os

import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import (
    RegisterSerializer, EmailVerificationSerializer, LoginSerializer, MyTokenObtainPairSerializer, ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer
)
from lemka.models import User
from lemka_api.utils import Utils


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # TODO - rediriger user vers front-end avec url et token d'activation.

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('users-auth-api:email-verify')

        absurl = 'https://' + current_site + relative_link + '?token=' + str(token)
        email_body_html = get_template('authentication/register_template.html').render(dict({
            'username': user.username,
            'url': absurl
        }))
        email_body = f'Bonjour {user.username}, cliquez sur le lien suivant pour activer votre compte ... {absurl}'
        data = {
            # 'email_body': email_body,
            'email_body': email_body_html,
            'to_email': user.email,
            'email_subject': "Vérification d'email"
        }
        Utils.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING
    )

    # noinspection PyMethodMayBeStatic
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        redirect_url = request.GET.get('redirect_url', 'http://localhost:8080/email-verify/')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return CustomRedirect(redirect_url + '?token_valid=True&message=Votre compte a été activé avec succès&token=' + token)
            # return Response({'email': 'Activé avec succès'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return CustomRedirect(redirect_url + '?token_valid=False&message=Activtaion expiré&token=' + token)
            # return Response({'error': 'Activtaion expiré'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return CustomRedirect(redirect_url + '?token_valid=False&message=Jeton invalide&token=' + token)
            # return Response({'error': 'Jeton invalide'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email, auth_provider='email').exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('users-auth-api:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'https://' + current_site + relative_link
            email_body_html = get_template('authentication/reset_password_template.html').render(dict({
                'username': user.username,
                'absurl': absurl,
                'redirect_url': redirect_url
            }))
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl + "?redirect_url=" + redirect_url
            data = {
                # 'email_body': email_body,
                'email_body': email_body_html,
                'to_email': user.email,
                'email_subject': 'Reset your passsword'
            }
            Utils.send_email(data)
        return Response({'success': 'Nous vous avons envoyé un lien pour réinitialiser votre mot de passe'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url + '?token_valid=True&message=Identifiants Valides&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': "Le jeton n'est pas valide, veuillez en demander un nouveau"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
