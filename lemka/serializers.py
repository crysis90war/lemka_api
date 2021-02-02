import decimal

from rest_framework import serializers

from lemka.models import *


class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'


class VilleSerializer(serializers.ModelSerializer):
    ref_pays = PaysSerializer

    class Meta:
        model = Ville
        fields = '__all__'


class EntrepriseLemkaSerializer(serializers.ModelSerializer):
    ref_ville = VilleSerializer

    class Meta:
        model = EntrepriseLemka
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    mensurations_count = serializers.SerializerMethodField(read_only=True)
    adresses_count = serializers.SerializerMethodField(read_only=True)
    ref_genre = GenreSerializer

    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']

    # noinspection PyMethodMayBeStatic
    def get_mensurations_count(self, instance):
        return instance.mensurations.count()

    # noinspection PyMethodMayBeStatic
    def get_adresses_count(self, instance):
        return instance.adresses.count()


class AdresseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adresse
        exclude = ['ref_user']


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = "__all__"


class RayonSerializer(serializers.ModelSerializer):
    # rayon_slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Rayon
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    # section_slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Section
        fields = '__all__'


class TypeProduitSerializer(serializers.ModelSerializer):
    # type_produit_slug = serializers.SlugField(read_only=True)

    class Meta:
        model = TypeProduit
        fields = '__all__'


class CatalogueSerializer(serializers.ModelSerializer):
    # catalogue = serializers.SerializerMethodField()
    ref_rayon = RayonSerializer
    ref_section = SectionSerializer
    ref_type_produit = TypeProduitSerializer

    class Meta:
        model = Catalogue
        fields = '__all__'

    # def get_ref_rayon(self, instance):
    #     return f'{instance.ref_rayon.rayon}'
    #
    # def get_ref_section(self, instance):
    #     return f'{instance.ref_section.section}'
    #
    # def get_ref_type_produit(self, instance):
    #     return f'{instance.ref_type_produit.type_produit}'
    # # noinspection PyMethodMayBeStatic
    # def get_catalogue(self, instance):
    #     return f'{instance.ref_rayon.rayon}/{instance.ref_section.section}/{instance.ref_type_produit.type_produit}'


class TagSerializer(serializers.ModelSerializer):
    # tag_slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Tag
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    ref_catalogue = CatalogueSerializer
    ref_tag = TagSerializer
    ref_type_service = TypeServiceSerializer
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    utilisateur_a_like = serializers.SerializerMethodField()
    images_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ['updated_at', 'likes']

    # noinspection PyMethodMayBeStatic
    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %b %Y")

    # noinspection PyMethodMayBeStatic
    def get_likes_count(self, instance):
        return instance.likes.count()

    def get_utilisateur_a_like(self, instance):
        request = self.context.get("request")
        return instance.likes.filter(pk=request.user.pk).exists()

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        images = ArticleImage.objects.filter(ref_article=instance)
        return images.count()

    # # noinspection PyMethodMayBeStatic
    # def get_catalogue(self, instance):
    #     rayon = instance.ref_catalogue.ref_rayon.rayon
    #     section = instance.ref_catalogue.ref_section.section
    #     type_produit = instance.ref_catalogue.ref_type_produit.type_produit
    #     return f'{rayon} - {section} - {type_produit}'

class ArticleImageSerializer(serializers.ModelSerializer):
    article_slug = serializers.SerializerMethodField()

    class Meta:
        model = ArticleImage
        fields = "__all__"

    # noinspection PyMethodMayBeStatic
    def get_article_slug(self, instance):
        return instance.ref_article.slug


class DemandeDevisSerializer(serializers.ModelSerializer):
    ref_user = serializers.StringRelatedField(read_only=True)
    numero_demande_devis = serializers.StringRelatedField(read_only=True)
    est_traite = serializers.BooleanField(read_only=True)

    class Meta:
        model = DemandeDevis
        fields = "__all__"


class DevisSerializer(serializers.ModelSerializer):
    numero_devis = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Devis
        exclude = ['id']


class DetailSerialiser(serializers.ModelSerializer):
    ref_devis = serializers.StringRelatedField(read_only=True)
    total_ht = serializers.SerializerMethodField()

    class Meta:
        model = Detail
        fields = '__all__'

    # noinspection PyMethodMayBeStatic
    def get_total_ht(self, instance):
        total = float(instance.prix_u_ht) * instance.quantite
        return round(decimal.Decimal(total), 2)


class RendezVousSerializer(serializers.ModelSerializer):
    ref_user = serializers.StringRelatedField(read_only=True)
    end = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RendezVous
        fields = "__all__"


class HoraireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Horaire
        fields = "__all__"


class AccompteDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccompteDemande
        fields = "__all__"


class CouleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Couleur
        fields = "__all__"


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"


class MercerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mercerie
        fields = "__all__"


class MercerieCouleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = MercerieOption
        fields = "__all__"


class MercerieCouleurImageSerializer(serializers.ModelSerializer):
    ref_mercerie_couleur = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOptionImage
        fields = "__all__"

    # noinspection PyMethodMayBeStatic
    def get_ref_mercerie_couleur(self, instance):
        ref_mercerie_couleur = instance.ref_mercerie_couleur.id
        return ref_mercerie_couleur


class TvaSertializer(serializers.ModelSerializer):
    class Meta:
        model = Tva
        fields = '__all__'


class MensurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mensuration
        fields = '__all__'


class UserMensurationSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserMensuration
        exclude = ['ref_user']


class MensurationUserMensurationSerializer(serializers.ModelSerializer):
    ref_mensuration = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MensurationUserMensuration
        exclude = ['ref_user_mensuration']


class ProfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)
    email = serializers.StringRelatedField(read_only=True)
    last_login = serializers.StringRelatedField(read_only=True)
    created_at = serializers.StringRelatedField(read_only=True)
    updated_at = serializers.StringRelatedField(read_only=True)
    is_verified = serializers.StringRelatedField(read_only=True)
    is_active = serializers.StringRelatedField(read_only=True)
    is_staff = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(read_only=True)
    # ref_genre = GenreSerializer(many=False)

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
        exclude = ['ref_user']


class CheckUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']