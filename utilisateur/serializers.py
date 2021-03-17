from rest_framework import serializers

from lemka.models import DemandeDevis


class UserDemandeDevisSerializer(serializers.ModelSerializer):
    numero_demande_devis = serializers.IntegerField(read_only=True)
    est_traite = serializers.BooleanField(default=False, read_only=True)
    est_urgent = serializers.BooleanField(default=False)
    est_soumis = serializers.BooleanField(default=False)

    class Meta:
        model = DemandeDevis
        exclude = ['ref_user']
