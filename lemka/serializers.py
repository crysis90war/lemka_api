from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import TokenError
from lemka import google, facebook
from lemka.models import *
from lemka.register import register_social_user


# region Auth



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {'username': "Le nom d'utilisateur ne doit contenir que des caractères alphanumériques"}

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'password2': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        if password != password2:
            raise serializers.ValidationError({
                'password': 'Les mots de passe doivent être identiques !'
            })
        return attrs

    def create(self, validated_data):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        return User.objects.create_user(email=email, username=username, password=password)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'is_staff', 'auth_provider']

    # noinspection PyMethodMayBeStatic
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Veuillez continuer votre connexion en utilisant ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed("Identifiants non valides, réessayez")
        if not user.is_active:
            raise AuthenticationFailed("Compte désactivé, contactez l'administrateur")
        if not user.is_verified:
            raise AuthenticationFailed("L'email n'est pas verifié")

        return {
            'email': user.email,
            'username': user.username,
            'is_staff': user.is_staff,
            'auth_provider': user.auth_provider,
            'tokens': user.tokens
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=5, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=5, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'password2', 'token', 'uidb64']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'password2': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Le lien de réinitialisation n'est pas valide", 401)

            user.set_password(password)
            user.save()

            return user

        except Exception as e:
            raise AuthenticationFailed("Le lien de réinitialisation n'est pas valide", 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_staff'] = user.is_staff
        token['email'] = user.email
        token['username'] = user.username
        token['auth_provider'] = user.auth_provider

        return token


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
        user_aud = user_data['aud']
        if user_aud != google_client_id:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider,
            user_id=user_id,
            email=email,
            name=name
        )


# endregion


# region Utilisateur

class UserArticleSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['ref_tags', 'likes']
        extra_kwargs = {
            'ref_service': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
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
    service = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    mensuration = serializers.SerializerMethodField(read_only=True)
    merceries = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DemandeDevis
        exclude = ['ref_user']
        extra_kwargs = {
            'numero_demande_devis': {'read_only': True},
            'est_traite': {'read_only': True, 'default': False},
            'ref_service': {'write_only': True},
            'ref_article': {'write_only': True},
            'ref_mensuration': {'write_only': True},
            'ref_merceries': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
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
    def get_merceries(self, instance):
        serializer = MercerieSerializer(instance.ref_merceries, many=True)
        return serializer.data


class UserDevisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = '__all__'


class UserDevisAccepterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devis
        fields = ['est_accepte']


class RendezVousExistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = ['start', 'end']


class AnnulerRendezVousSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField(read_only=True)
    devis = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RendezVous
        exclude = ['ref_user', 'ref_devis', 'ref_service']
        extra_kwargs = {
            'date': {'read_only': True},
            'start': {'read_only': True},
            'end': {'read_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_devis(self, instance):
        if instance.ref_devis:
            serializer = UserDevisSerializer(instance.ref_devis)
            return serializer.data
        else:
            return None


class UserRendezVousSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField(read_only=True)
    devis = serializers.SerializerMethodField(read_only=True)
    est_annule = serializers.BooleanField(default=False)

    class Meta:
        model = RendezVous
        exclude = ['ref_user']
        extra_kwargs = {
            'end': {'read_only': True},
            'ref_service': {'write_only': True},
            'ref_devis': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_devis(self, instance):
        if instance.ref_devis:
            serializer = UserDevisSerializer(instance.ref_devis)
            return serializer.data
        else:
            return None


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
    genre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ['id', 'groups', 'user_permissions', 'auth_provider', 'last_login']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_verified': {'read_only': True},
            'is_active': {'read_only': True},
            'email': {'read_only': True},
            'ref_genre': {'write_only': True},
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
        queryset = UserMesure.objects.filter(ref_user_mensuration=instance)
        serializer = UserMesureSerializer(queryset, many=True)
        return serializer.data


class UserMesureSerializer(serializers.ModelSerializer):
    mensuration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMesure
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


# endregion

class GlobalMercerieSerializer(serializers.ModelSerializer):
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    reference = serializers.CharField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    tva = serializers.SerializerMethodField(read_only=True)
    couleur = serializers.SerializerMethodField(read_only=True)
    categorie = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mercerie
        exclude = ['ref_tva', 'ref_couleur', 'ref_categorie']

    # noinspection PyMethodMayBeStatic
    def get_caracteristiques(self, instance):
        data = instance.caracteristiques.filter(ref_mercerie=instance)
        serializer = MercerieCaracteristiqueSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = MercerieImage.objects.filter(ref_mercerie=instance).order_by('is_main')
        serializer = MercerieImageSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_tva(self, instance):
        seralizer = TvaSertializer(instance.ref_tva)
        return seralizer.data

    # noinspection PyMethodMayBeStatic
    def get_couleur(self, instance):
        serializer = CouleurSerializer(instance.ref_couleur)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_categorie(self, instance):
        serializer = CategorieSerializer(instance.ref_categorie)
        return serializer.data


class GlobalArticleSerializer(serializers.ModelSerializer):
    user_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['likes', 'ref_service', 'ref_tags']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'titre': {'read_only': True},
            'description': {'read_only': True},
            'est_active': {'read_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_user_liked(self, instance):
        request = self.context.get("request")
        return instance.likes.filter(pk=request.user.pk).exists()

    # noinspection PyMethodMayBeStatic
    def get_likes_count(self, instance):
        return instance.likes.count()

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        images = ArticleImage.objects.filter(ref_article=instance)
        return images.count()

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = ArticleImage.objects.filter(ref_article=instance).order_by('-is_main')
        serializer = ArticleImageSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_tags(self, instance):
        if instance.ref_tags is not None:
            serializer = TagSerializer(instance.ref_tags, many=True)
            return serializer.data
        else:
            return []

# region Admin


class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'


class VilleSerializer(serializers.ModelSerializer):
    pays = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ville
        fields = '__all__'
        extra_kwargs = {
            'ref_pays': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_pays(self, instance):
        serializer = PaysSerializer(instance.ref_pays)
        return serializer.data


class EntrepriseLemkaSerializer(serializers.ModelSerializer):
    ville = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entreprise
        fields = "__all__"
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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    mensurations_count = serializers.SerializerMethodField(read_only=True)
    genre = serializers.SerializerMethodField(read_only=True)

    # adresse = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups', 'last_login']
        extra_kwargs = {
            'ref_genre': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_mensurations_count(self, instance):
        return instance.mensurations.count()

    # noinspection PyMethodMayBeStatic
    def get_genre(self, instance):
        if instance.ref_genre is not None:
            serializer = GenreSerializer(instance.ref_genre)
            return serializer.data
        else:
            return None


class AdminUserMesureSerializer(serializers.ModelSerializer):
    mensuration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMesure
        exclude = ['ref_user_mensuration', 'ref_mensuration']

    # noinspection PyMethodMayBeStatic
    def get_mensuration(self, instance):
        return instance.ref_mensuration.nom


class AdminUserMensurationSerializer(serializers.ModelSerializer):
    mesures = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMensuration
        exclude = ['ref_user']

    # noinspection PyMethodMayBeStatic
    def get_mesures(self, instance):
        queryset = UserMesure.objects.filter(ref_user_mensuration=instance)
        serializer = AdminUserMesureSerializer(queryset, many=True)
        return serializer.data


class AdminDemandeDevisSerializer(serializers.ModelSerializer):
    numero_demande_devis = serializers.StringRelatedField(read_only=True)
    utilisateur = serializers.SerializerMethodField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    mensuration = serializers.SerializerMethodField(read_only=True)
    merceries = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DemandeDevis
        fields = "__all__"
        extra_kwargs = {
            'ref_user': {'read_only': True},
            'ref_service': {'write_only': True},
            'ref_article': {'write_only': True},
            'ref_merceries': {'write_only': True},
            'ref_mensuration': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_utilisateur(self, instance):
        if instance.ref_user.first_name and instance.ref_user.last_name:
            full_name = f'{instance.ref_user.first_name} {instance.ref_user.last_name}'
            return full_name
        else:
            return instance.ref_user.username

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_article(self, instance):
        if instance.ref_article is not None:
            print(instance.ref_article)
            serializer = ArticleSerializer(instance.ref_article)
            return serializer.data
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def get_mensuration(self, instance):
        if instance.ref_mensuration is not None:
            serializer = AdminUserMensurationSerializer(instance.ref_mensuration)
            return serializer.data
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def get_merceries(self, instance):
        serializer = MercerieSerializer(instance.ref_merceries, many=True)
        return serializer.data


class AdminDevisSerializer(serializers.ModelSerializer):
    numero_demande_devis = serializers.SerializerMethodField(read_only=True)
    demande_devis_titre = serializers.SerializerMethodField(read_only=True)
    details = serializers.SerializerMethodField(read_only=True)
    demande_devis = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Devis
        fields = '__all__'
        extra_kwargs = {
            'est_accepte': {'read_only': True},
            'numero_devis': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'ref_demande_devis': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_numero_demande_devis(self, instance):
        return f'{instance.ref_demande_devis.numero_demande_devis}'

    # noinspection PyMethodMayBeStatic
    def get_details(self, instance):
        data = Detail.objects.filter(ref_devis=instance)
        serializer = DetailSerialiser(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_demande_devis_titre(self, instance):
        return f'{instance.ref_demande_devis.titre}'

    # noinspection PyMethodMayBeStatic
    def get_demande_devis(self, instance):
        serializer = AdminDemandeDevisSerializer(instance.ref_demande_devis)
        return serializer.data


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class RayonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rayon
        fields = "__all__"


class TypeProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduit
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class AdminAdresseSerializer(serializers.ModelSerializer):
    ville = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Adresse
        exclude = ['ref_user']
        extra_kwargs = {
            'ref_ville': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_ville(self, instance):
        if instance and instance.ref_ville:
            serializer = VilleSerializer(instance.ref_ville)
            return serializer.data


class CaracteristiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristique
        fields = "__all__"


class HoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horaire
        fields = "__all__"
        extra_kwargs = {
            'jour': {'read_only': True},
            'jour_semaine': {'read_only': True},
        }


class CouleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Couleur
        fields = "__all__"


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"


class TvaSertializer(serializers.ModelSerializer):
    class Meta:
        model = Tva
        fields = '__all__'


class DetailSerialiser(serializers.ModelSerializer):
    tva = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Detail
        exclude = ['ref_devis']
        extra_kwargs = {
            'ref_tva': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_tva(self, instance):
        serializer = TvaSertializer(instance.ref_tva)
        return serializer.data


class MensurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensuration
        fields = '__all__'


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ['ref_article']


class ArticleSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField(read_only=True)
    rayon = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    type_produit = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['likes']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'slug': {'read_only': True},
            'ref_service': {'write_only': True},
            'ref_rayon': {'write_only': True},
            'ref_section': {'write_only': True},
            'ref_type_produit': {'write_only': True},
            'ref_tags': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_rayon(self, instance):
        serializer = RayonSerializer(instance.ref_rayon)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_section(self, instance):
        serializer = SectionSerializer(instance.ref_section)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_type_produit(self, instance):
        serializer = TypeProduitSerializer(instance.ref_type_produit)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_likes_count(self, instance):
        return instance.likes.count()

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        images = ArticleImage.objects.filter(ref_article=instance)
        return images.count()

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = ArticleImage.objects.filter(ref_article=instance).order_by('-is_main')
        serializer = ArticleImageSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_tags(self, instance):
        if instance.ref_tags is not None:
            serializer = TagSerializer(instance.ref_tags, many=True)
            return serializer.data
        else:
            return []


class MercerieSerializer(serializers.ModelSerializer):
    tva = serializers.SerializerMethodField(read_only=True)
    couleur = serializers.SerializerMethodField(read_only=True)
    categorie = serializers.SerializerMethodField(read_only=True)
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mercerie
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'reference': {'read_only': True},
            'ref_tva': {'write_only': True},
            'ref_couleur': {'write_only': True},
            'ref_categorie': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_caracteristiques(self, instance):
        data = instance.caracteristiques.filter(ref_mercerie=instance)
        serializer = MercerieCaracteristiqueSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        return instance.images.count()

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = MercerieImage.objects.filter(ref_mercerie=instance).order_by('-is_main')
        serializer = MercerieImageSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_tva(self, instance):
        seralizer = TvaSertializer(instance.ref_tva)
        return seralizer.data

    # noinspection PyMethodMayBeStatic
    def get_couleur(self, instance):
        serializer = CouleurSerializer(instance.ref_couleur)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_categorie(self, instance):
        serializer = CategorieSerializer(instance.ref_categorie)
        return serializer.data


class MercerieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MercerieImage
        exclude = ['ref_mercerie']


class MercerieCaracteristiqueSerializer(serializers.ModelSerializer):
    caracteristique = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieCaracteristique
        exclude = ['ref_mercerie']
        extra_kwargs = {
            'ref_caracteristique': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_caracteristique(self, instance):
        serializer = CaracteristiqueSerializer(instance.ref_caracteristique)
        data = serializer.data
        return data


class AdminRendezVousSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField(read_only=True)
    devis = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RendezVous
        fields = '__all__'
        extra_kwargs = {
            'ref_service': {'write_only': True},
            'ref_devis': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_service(self, instance):
        serializer = ServiceSerializer(instance.ref_service)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_devis(self, instance):
        if instance.ref_devis:
            serializer = AdminDevisSerializer(instance.ref_devis)
            return serializer.data
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def get_user(self, instance):
        if instance.ref_user:
            serializer = UserSerializer(instance.ref_user)
            return serializer.data


# endregion