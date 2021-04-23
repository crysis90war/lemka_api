from rest_framework import serializers

from administrateur.serializers import (
    MercerieCaracteristiqueSerializer, MercerieImageSerializer, TvaSertializer, CouleurSerializer
)
from lemka.models import (
    Mercerie, MercerieImage
)


class GlobalMercerieSerializer(serializers.ModelSerializer):
    caracteristiques = serializers.SerializerMethodField(read_only=True)
    reference = serializers.CharField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    tva = serializers.SerializerMethodField(read_only=True)
    couleur = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mercerie
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
