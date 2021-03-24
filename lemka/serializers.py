from rest_framework import serializers

from administrateur.serializers import MercerieOptionCaracteristiqueSerializer, MercerieOptionImageSerializer
from lemka.models import *


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


class GlobalMerceriesSerializer(serializers.ModelSerializer):
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOption
        fields = '__all__'

    # noinspection PyMethodMayBeStatic
    def get_name(self, instance):
        name = instance.ref_mercerie.nom
        couleur = instance.ref_couleur.nom
        return f'{name} - {couleur}'

    def get_caracteristiques(self, instance):
        data = instance.catacteristiques.filter(ref_mercerie_option=instance)
        serializer = MercerieOptionCaracteristiqueSerializer(data, many=True)
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def get_images(self, instance):
        data = MercerieOptionImage.objects.filter(ref_mercerie_option=instance).order_by('is_main')
        serializer = MercerieOptionImageSerializer(data, many=True)
        return serializer.data
