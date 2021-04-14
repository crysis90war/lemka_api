from rest_framework import serializers

from administrateur.serializers import (
    GenreSerializer, VilleSerializer, TypeServiceSerializer, CatalogueSerializer, ArticleImageSerializer, MercerieOptionSerializer
)
from lemka.models import (
    DemandeDevis, RendezVous, Adresse, User, UserMensuration, UserMensurationMesure, Devis, Article, ArticleImage
)


class UserArticleSerializer(serializers.ModelSerializer):
    catalogue = serializers.SerializerMethodField(read_only=True)
    type_service = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['ref_tag', 'likes']
        extra_kwargs = {
            'ref_catalogue': {'write_only': True},
            'ref_type_service': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_catalogue(self, instance):
        serializer = CatalogueSerializer(instance.ref_catalogue)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_type_service(self, instance):
        serializer = TypeServiceSerializer(instance.ref_type_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = ArticleImage.objects.filter(ref_article=instance).order_by('is_main')
        serializer = ArticleImageSerializer(data, many=True)
        return serializer.data


class UserDemandeDevisSerializer(serializers.ModelSerializer):
    est_urgent = serializers.BooleanField(default=False)
    est_soumis = serializers.BooleanField(default=False)
    en_cours = serializers.BooleanField(default=False, read_only=True)
    type_service = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    mensuration = serializers.SerializerMethodField(read_only=True)
    mercerie_options = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DemandeDevis
        exclude = ['ref_user']
        extra_kwargs = {
            'numero_demande_devis': {'read_only': True},
            'est_traite': {'read_only': True, 'default': False},
            'ref_type_service': {'write_only': True},
            'ref_article': {'write_only': True},
            'ref_mensuration': {'write_only': True},
            'ref_mercerie_options': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_type_service(self, instance):
        serializer = TypeServiceSerializer(instance.ref_type_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_article(self, instance):
        if instance.ref_article is not None:
            serializer = UserArticleSerializer(instance.ref_article)
            return serializer.data
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def get_mensuration(self, instance):
        if instance.ref_mensuration is not None:
            serializer = UserMensurationSerializer(instance.ref_mensuration)
            return serializer.data
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def get_mercerie_options(self, instance):
        serializer = MercerieOptionSerializer(instance.ref_mercerie_options, many=True)
        return serializer.data


class UserDevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = '__all__'


class UserRendezVousSerializer(serializers.ModelSerializer):
    ref_user = serializers.StringRelatedField(read_only=True)
    end = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RendezVous
        fields = "__all__"


class AdresseSerializer(serializers.ModelSerializer):
    ville = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Adresse
        exclude = ['ref_user']
        extra_kwargs = {
            'ref_ville': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_ville(self, instance):
        if instance.ref_ville is not None:
            serializer = VilleSerializer(instance.ref_ville)
            return serializer.data
        else:
            return None


class ProfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.StringRelatedField(read_only=True)
    last_login = serializers.StringRelatedField(read_only=True)
    created_at = serializers.StringRelatedField(read_only=True)
    updated_at = serializers.StringRelatedField(read_only=True)
    is_verified = serializers.StringRelatedField(read_only=True)
    is_active = serializers.StringRelatedField(read_only=True)
    is_staff = serializers.StringRelatedField(read_only=True)
    genre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ['id', 'groups', 'user_permissions', 'auth_provider', 'is_superuser']
        extra_kwargs = {
            'ref_genre': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_genre(self, instance):
        if instance.ref_genre is not None:
            serializer = GenreSerializer(instance.ref_genre)
            return serializer.data
        else:
            return None


class UserMensurationSerializer(serializers.ModelSerializer):
    mesures = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMensuration
        exclude = ['ref_user']

    # noinspection PyMethodMayBeStatic
    def get_mesures(self, instance):
        queryset = UserMensurationMesure.objects.filter(ref_user_mensuration=instance)
        serializer = UserMensurationMesureSerializer(queryset, many=True)
        return serializer.data


class UserMensurationMesureSerializer(serializers.ModelSerializer):
    mensuration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMensurationMesure
        exclude = ['ref_user_mensuration', 'ref_mensuration']

    # noinspection PyMethodMayBeStatic
    def get_mensuration(self, instance):
        return instance.ref_mensuration.nom


class UserAdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = ['ref_user', 'id']


class UserCreateAdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = ['id']


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image']
