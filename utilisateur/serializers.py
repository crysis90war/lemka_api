from rest_framework import serializers

from lemka.models import DemandeDevis, RendezVous, Adresse, User, UserMensuration, MensurationUserMensuration


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


class UserRendezVousSerializer(serializers.ModelSerializer):
    ref_user = serializers.StringRelatedField(read_only=True)
    end = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RendezVous
        fields = "__all__"


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = ['ref_user']


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
