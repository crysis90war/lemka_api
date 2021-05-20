import os
import random

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from lemka.models import User


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email,
                password=os.environ.get('SOCIAL_SECRET')
            )

            return get_tokens(registered_user)

        else:
            raise AuthenticationFailed(
                detail='Veuillez continuer votre connexion en utilisant ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email,
            password=os.environ.get('SOCIAL_SECRET')
        )
        return get_tokens(new_user)


def get_tokens(user):
    serializer = TokenObtainPairSerializer()
    token = serializer.get_token(user)
    token['is_staff'] = user.is_staff
    token['email'] = user.email
    token['username'] = user.username

    return {
        'refresh': str(token),
        'access': str(token.access_token)
    }
