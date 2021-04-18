from rest_framework import serializers

from lemka.models import (
    Pays, Ville, EntrepriseLemka, Genre, User, DemandeDevis, Devis, TypeService, Rayon, Section, TypeProduit, Tag, Adresse, Caracteristique,
    Catalogue, Couleur, Categorie, Horaire, Detail, Tva, Mensuration, ArticleImage, Article, Mercerie, MercerieOption, MercerieOptionImage,
    MercerieOptionCaracteristique, UserMensuration, UserMensurationMesure
)


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
        model = EntrepriseLemka
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

    # # noinspection PyMethodMayBeStatic
    # def get_adresse(self, instance):
    #     if Adresse.objects.filter(ref_user=instance).exists():
    #         queryset = Adresse.objects.get(ref_user=instance)
    #         serializer = AdminAdresseSerializer(queryset)
    #         return serializer.data


class AdminUserMensurationMesureSerializer(serializers.ModelSerializer):
    mensuration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMensurationMesure
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
        queryset = UserMensurationMesure.objects.filter(ref_user_mensuration=instance)
        serializer = AdminUserMensurationMesureSerializer(queryset, many=True)
        return serializer.data


class AdminDemandeDevisSerializer(serializers.ModelSerializer):
    numero_demande_devis = serializers.StringRelatedField(read_only=True)
    utilisateur = serializers.SerializerMethodField(read_only=True)
    type_service = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)
    mensuration = serializers.SerializerMethodField(read_only=True)
    mercerie_options = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DemandeDevis
        fields = "__all__"
        extra_kwargs = {
            'ref_user': {'read_only': True},
            'ref_type_service': {'write_only': True},
            'ref_article': {'write_only': True},
            'ref_mercerie_options': {'write_only': True},
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
    def get_type_service(self, instance):
        serializer = TypeServiceSerializer(instance.ref_type_service)
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
    def get_mercerie_options(self, instance):
        serializer = MercerieOptionSerializer(instance.ref_mercerie_options, many=True)
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


class CatalogueSerializer(serializers.ModelSerializer):
    rayon = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    type_produit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Catalogue
        fields = '__all__'
        extra_kwargs = {
            'ref_rayon': {'write_only': True},
            'ref_section': {'write_only': True},
            'ref_type_produit': {'write_only': True},
        }

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
    likes_count = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    catalogue = serializers.SerializerMethodField(read_only=True)
    type_service = serializers.SerializerMethodField(read_only=True)
    rayon = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    type_produit = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        exclude = ['likes']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'slug': {'read_only': True},
            'ref_catalogue': {'write_only': True},
            'ref_article': {'write_only': True},
            'ref_type_service': {'write_only': True},
            'ref_tag': {'write_only': True},
        }

    # noinspection PyMethodMayBeStatic
    def get_likes_count(self, instance):
        return instance.likes.count()

    # noinspection PyMethodMayBeStatic
    def get_images_count(self, instance):
        images = ArticleImage.objects.filter(ref_article=instance)
        return images.count()

    # noinspection PyMethodMayBeStatic
    def get_catalogue(self, instance):
        serializer = CatalogueSerializer(instance.ref_catalogue)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_type_service(self, instance):
        serializer = TypeServiceSerializer(instance.ref_type_service)
        return serializer.data

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
        data = ArticleImage.objects.filter(ref_article=instance).order_by('-is_main')
        serializer = ArticleImageSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_tags(self, instance):
        if instance.ref_tag is not None:
            serializer = TagSerializer(instance.ref_tag, many=True)
            return serializer.data
        else:
            return []


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

    # noinspection PyMethodMayBeStatic
    def get_options_count(self, instance):
        return instance.options.count()


class MercerieOptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    tva = serializers.SerializerMethodField(read_only=True)
    couleur = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOption
        exclude = ['ref_mercerie']
        extra_kwargs = {
            'id': {'read_only': True},
            'ref_tva': {'write_only': True},
            'ref_couleur': {'write_only': True},
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

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = MercerieOptionImage.objects.filter(ref_mercerie_option=instance).order_by('is_main')
        serializer = MercerieOptionImageSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_tva(self, instance):
        seralizer = TvaSertializer(instance.ref_tva)
        return seralizer.data

    # noinspection PyMethodMayBeStatic
    def get_couleur(self, instance):
        serializer = CouleurSerializer(instance.ref_couleur)
        return serializer.data


class MercerieOptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MercerieOptionImage
        fields = "__all__"


class MercerieOptionCaracteristiqueSerializer(serializers.ModelSerializer):
    caracteristique = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOptionCaracteristique
        exclude = ['ref_mercerie_option']
        extra_kwargs = {
            'ref_caracteristique': {'write_only': True}
        }

    # noinspection PyMethodMayBeStatic
    def get_caracteristique(self, instance):
        return instance.ref_caracteristique.nom
