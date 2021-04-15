from rest_framework import serializers

from administrateur.serializers import MercerieOptionCaracteristiqueSerializer, MercerieOptionImageSerializer, TvaSertializer, \
    CouleurSerializer
from lemka.models import *


class GlobalMerceriesSerializer(serializers.ModelSerializer):
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    reference = serializers.CharField()
    images = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    tva = serializers.SerializerMethodField(read_only=True)
    couleur = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MercerieOption
        fields = '__all__'
        extra_kwarges = {
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

