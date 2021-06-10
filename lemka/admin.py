from django.apps import apps
from django.contrib import admin

from .models import (
    User, Horaire, UserMensuration, UserMesure, Adresse, Service, Tva, Ville, Article, ArticleImage,
    DemandeDevis, MercerieCaracteristique, RendezVous, Detail, Entreprise, Mercerie, MercerieImage
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'is_superuser', 'is_staff', 'is_active', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'auth_provider', 'is_staff', 'is_superuser']
    ordering = ['-created_at']


@admin.register(Horaire)
class HoraireAdmin(admin.ModelAdmin):
    list_display = ['jour', 'heure_ouverture', 'pause_debut', 'pause_fin', 'heure_fermeture', 'sur_rdv', 'est_ferme']
    ordering = ['jour_semaine']


@admin.register(UserMensuration)
class UserMensurationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'is_main']
    list_filter = ['is_main']
    ordering = ['ref_user__email', 'is_main']

    def user(self, obj):
        return obj.ref_user.email


@admin.register(UserMesure)
class UserMesureAdmin(admin.ModelAdmin):
    list_display = ['mesure', 'mensuration', 'user_mensuration', 'user']
    ordering = ['ref_user_mensuration__ref_user__username', '-ref_user_mensuration__is_main', 'ref_mensuration__id']

    def mensuration(self, obj):
        return obj.ref_mensuration.nom

    def user_mensuration(self, obj):
        return obj.ref_user_mensuration.titre

    def user(self, obj):
        return obj.ref_user_mensuration.ref_user.email


@admin.register(Adresse)
class AdresseAdmin(admin.ModelAdmin):
    list_display = ['user', 'ville', 'rue', 'numero', 'boite']

    def ville(self, obj):
        return obj.ref_ville.ville

    def user(self, obj):
        return obj.ref_user.email


@admin.register(Service)
class TypeServiceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'duree_minute']


@admin.register(Tva)
class TvaAdmin(admin.ModelAdmin):
    list_display = ['id', 'taux', 'applicable']
    ordering = ['taux']


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['ville', 'code_postale']
    ordering = ['code_postale']
    search_fields = ['ville', 'code_postale']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['slug', 'titre', 'service', 'est_active']
    list_filter = ['est_active', 'ref_service']
    search_fields = ['titre', 'description']

    def service(self, obj):
        return obj.ref_service.nom


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'image', 'is_main']
    ordering = ['ref_article__titre', 'is_main']
    list_filter = ['is_main']
    search_fields = ['ref_article__titre']

    def article(self, obj):
        return obj.ref_article.slug


@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):
    list_display = ['numero_demande_devis', 'titre', 'est_urgent', 'est_soumis', 'en_cours', 'est_traite', 'created_at']
    list_filter = ['est_urgent', 'est_soumis', 'en_cours', 'est_traite']
    search_fields = ['numero_demande_devis', 'titre']


@admin.register(Mercerie)
class MercerieAdmin(admin.ModelAdmin):
    list_display = ['reference', 'categorie', 'nom', 'est_publie']
    list_filter = ['est_publie', 'ref_categorie']

    def categorie(self, obj):
        return obj.ref_categorie.nom


@admin.register(MercerieImage)
class MercerieImageAdmin(admin.ModelAdmin):
    list_display = ['mercerie', 'image', 'is_main']
    list_filter = ['is_main', 'ref_mercerie__nom']
    ordering = ['ref_mercerie__nom', 'is_main']

    def mercerie(self, obj):
        return obj.ref_mercerie.nom


@admin.register(MercerieCaracteristique)
class MercerieCaracteristiqueAdmin(admin.ModelAdmin):
    list_display = ['reference', 'mercerie', 'caracteristique', 'valeur']
    ordering = ['ref_mercerie__reference', 'ref_caracteristique__nom']
    search_fields = ['ref_mercerie__reference', 'ref_caracteristique__nom']

    def reference(self, obj):
        return obj.ref_mercerie.reference

    def mercerie(self, obj):
        return obj.ref_mercerie.nom

    def caracteristique(self, obj):
        return obj.ref_caracteristique.nom


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'service', 'date', 'start', 'end', 'est_annule']
    ordering = ['-date', '-start']
    list_filter = ['est_annule']

    def utilisateur(self, obj):
        return obj.ref_user.email

    def service(self, obj):
        return obj.ref_service.nom


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['designation', 'prix_u_ht', 'quantite', 'devis', 'tva']
    list_filter = ['ref_devis__numero_devis']
    search_fields = ['ref_devis__numero_devis']

    def devis(self, obj):
        return obj.ref_devis.numero_devis

    def tva(self, obj):
        return obj.ref_tva.taux


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_societe', 'facebook', 'instagram', 'twitter', 'linkedin']

    def facebook(self, obj):
        if len(obj.facebook_link) == 0:
            return False
        else:
            return True

    def instagram(self, obj):
        if len(obj.instagram_link) == 0:
            return False
        else:
            return True

    def twitter(self, obj):
        if len(obj.twitter_link) == 0:
            return False
        else:
            return True

    def linkedin(self, obj):
        if len(obj.linkedin_link) == 0:
            return False
        else:
            return True

    facebook.boolean = True
    instagram.boolean = True
    twitter.boolean = True
    linkedin.boolean = True


models = apps.get_models()
admin.site.site_header = "Lemka - Atelier de couture"

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
