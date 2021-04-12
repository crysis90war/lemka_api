from rest_framework import serializers

from administrateur.serializers import MercerieOptionCaracteristiqueSerializer, MercerieOptionImageSerializer
from lemka.models import *


class GlobalMerceriesSerializer(serializers.ModelSerializer):
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    reference = serializers.CharField()
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
