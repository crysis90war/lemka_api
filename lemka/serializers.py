from rest_framework import serializers

from administrateur.serializers import (
    MercerieCaracteristiqueSerializer, MercerieImageSerializer, TvaSertializer, CouleurSerializer,
    TypeServiceSerializer, ArticleImageSerializer, TagSerializer, CategorieSerializer
)
from lemka.models import (
    Mercerie, MercerieImage, Article, ArticleImage
)


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
        data = instance.catacteristiques.filter(ref_mercerie=instance)
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
        serializer = TypeServiceSerializer(instance.ref_service)
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
