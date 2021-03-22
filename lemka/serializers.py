import decimal

from rest_framework import serializers

from administrateur.serializers import RayonSerializer, SectionSerializer, TypeProduitSerializer
from lemka.models import *


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = ['ref_user']


class ArticleListSerializer(serializers.ModelSerializer):
    created_at = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    type_service = serializers.SerializerMethodField(read_only=True)
    rayon = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    type_produit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['updated_at', 'likes', 'ref_tag']

    # noinspection PyMethodMayBeStatic
    def get_likes_count(self, instance):
        return instance.likes.count()

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        images = ArticleImage.objects.filter(ref_article=instance)
        return images.count()

    # noinspection PyMethodMayBeStatic
    def get_type_service(self, instance):
        return instance.ref_type_service.type_service

    # noinspection PyMethodMayBeStatic
    def get_rayon(self, instance):
        return instance.ref_catalogue.ref_rayon.rayon

    # noinspection PyMethodMayBeStatic
    def get_section(self, instance):
        return instance.ref_catalogue.ref_section.section

    # noinspection PyMethodMayBeStatic
    def get_type_produit(self, instance):
        return instance.ref_catalogue.ref_type_produit.type_produit


class UserMensurationSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserMensuration
        exclude = ['ref_user']


class MensurationUserMensurationSerializer(serializers.ModelSerializer):
    mensuration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MensurationUserMensuration
        exclude = ['ref_user_mensuration', 'ref_mensuration']

    def get_mensuration(self, instance):
        return instance.ref_mensuration.nom


class ProfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.StringRelatedField(read_only=True)
    last_login = serializers.StringRelatedField(read_only=True)
    created_at = serializers.StringRelatedField(read_only=True)
    updated_at = serializers.StringRelatedField(read_only=True)
    is_verified = serializers.StringRelatedField(read_only=True)
    is_active = serializers.StringRelatedField(read_only=True)
    is_staff = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        exclude = ['id', 'groups', 'user_permissions', 'auth_provider', 'is_superuser']


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image']


class UserAdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = ['ref_user', 'id']


class UserCreateAdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = ['id']


class CheckUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
