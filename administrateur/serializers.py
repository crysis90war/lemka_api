import decimal

from rest_framework import serializers

from lemka.models import (
    Pays, Ville, EntrepriseLemka, Genre, User, DemandeDevis, Devis, TypeService, Rayon, Section, TypeProduit, Tag, Adresse, Caracteristique,
    Catalogue, Couleur, Categorie, Horaire, Detail, Tva, Mensuration, ArticleImage, Article, Mercerie, MercerieOption, MercerieOptionImage,
    MercerieOptionCaracteristique
)


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
    created_at = serializers.SerializerMethodField(read_only=True)

    # updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']

    # noinspection PyMethodMayBeStatic
    def get_mensurations_count(self, instance):
        return instance.mensurations.count()

    # noinspection PyMethodMayBeStatic
    def get_adresses_count(self, instance):
        return instance.adresses.count()

    # noinspection PyMethodMayBeStatic
    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %b %Y")

    # noinspection PyMethodMayBeStatic
    def get_updated_at(self, instance):
        return instance.updated_at.strftime("%d %b %Y")


class AdminDemandeDevisSerializer(serializers.ModelSerializer):
    numero_demande_devis = serializers.StringRelatedField(read_only=True)
    utilisateur = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DemandeDevis
        fields = "__all__"
        extra_kwargs = {
            'ref_user': {'read_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_utilisateur(self, instance):
        if instance.ref_user.first_name and instance.ref_user.last_name:
            full_name = f'{instance.ref_user.first_name} {instance.ref_user.last_name}'
            return full_name
        else:
            return instance.ref_user.username


class DevisSerializer(serializers.ModelSerializer):
    numero_devis = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Devis
        fields = '__all__'


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
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
    class Meta:
        model = Adresse
        exclude = ['ref_user']


class CaracteristiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristique
        fields = "__all__"


class CatalogueSerializer(serializers.ModelSerializer):
    rayon = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    type_produit = serializers.SerializerMethodField(read_only=True)
    ref_rayon = RayonSerializer
    ref_section = SectionSerializer
    ref_type_produit = TypeProduitSerializer

    class Meta:
        model = Catalogue
        fields = '__all__'

    # noinspection PyMethodMayBeStatic
    def get_rayon(self, instance):
        return f'{instance.ref_rayon.rayon}'

    # noinspection PyMethodMayBeStatic
    def get_section(self, instance):
        return f'{instance.ref_section.section}'

    # noinspection PyMethodMayBeStatic
    def get_type_produit(self, instance):
        return f'{instance.ref_type_produit.type_produit}'


class CouleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Couleur
        fields = "__all__"


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"


class HoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horaire
        fields = "__all__"


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


class TvaSertializer(serializers.ModelSerializer):
    class Meta:
        model = Tva
        fields = '__all__'


class MensurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensuration
        fields = '__all__'


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ['ref_article']


class ArticleSerializer(serializers.ModelSerializer):
    created_at = serializers.StringRelatedField(read_only=True)
    updated_at = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    type_service = serializers.SerializerMethodField(read_only=True)
    rayon = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    type_produit = serializers.SerializerMethodField(read_only=True)
    utilisateur_a_like = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['likes']

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

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = ArticleImage.objects.filter(ref_article=instance).order_by('is_main')
        serializer = ArticleImageSerializer(data, many=True)
        return serializer.data


class MercerieSerializer(serializers.ModelSerializer):
    nom = serializers.CharField()
    est_publie = serializers.BooleanField(default=False)
    categorie = serializers.SerializerMethodField(read_only=True)
    options_count = serializers.SerializerMethodField(read_only=True)
    ref_categorie = CategorieSerializer

    class Meta:
        model = Mercerie
        fields = '__all__'

    # noinspection PyMethodMayBeStatic
    def get_categorie(self, instance):
        return instance.ref_categorie.nom

    def get_options_count(self, instance):
        return instance.options.count()


class MercerieOptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOption
        exclude = ['ref_mercerie']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_name(self, instance):
        name = instance.ref_mercerie.nom
        couleur = instance.ref_couleur.nom
        return f'{name} - {couleur}'

    # noinspection PyMethodMayBeStatic
    def get_caracteristiques(self, instance):
        data = instance.catacteristiques.filter(ref_mercerie_option=instance)
        serializer = MercerieOptionCaracteristiqueSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        return instance.images.count()


class MercerieOptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MercerieOptionImage
        fields = "__all__"


class MercerieOptionCaracteristiqueSerializer(serializers.ModelSerializer):
    caracteristique = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOptionCaracteristique
        exclude = ['ref_mercerie_option']

    # noinspection PyMethodMayBeStatic
    def get_caracteristique(self, instance):
        return instance.ref_caracteristique.nom
