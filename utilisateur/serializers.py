from rest_framework import serializers

from administrateur.serializers import GenreSerializer, VilleSerializer
from lemka.models import (
    DemandeDevis, RendezVous, Adresse, User, UserMensuration, UserMensurationMesure, Devis
)


class UserDemandeDevisSerializer(serializers.ModelSerializer):
    est_traite = serializers.BooleanField(default=False, read_only=True)
    est_urgent = serializers.BooleanField(default=False)
    est_soumis = serializers.BooleanField(default=False)

    class Meta:
        model = DemandeDevis
        exclude = ['ref_user']
        extra_kwargs = {
            'numero_demande_devis': {'read_only': True}
        }


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

    def get_genre(self, instance):
        if instance.ref_genre is not None:
            serializer = GenreSerializer(instance.ref_genre)
            return serializer.data
        else:
            return None


class UserMensurationSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserMensuration
        exclude = ['ref_user']


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
