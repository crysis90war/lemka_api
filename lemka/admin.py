from django.contrib import admin
from django.apps import apps
from .models import User, Horaire, UserMensuration, Catalogue, UserMesure, Adresse, Ville


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'is_superuser', 'is_staff', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'auth_provider', 'is_staff', 'is_superuser']
    ordering = ['-created_at']


@admin.register(Horaire)
class HoraireAdmin(admin.ModelAdmin):
    list_display = ['jour_semaine', 'jour', 'heure_ouverture', 'pause_debut', 'pause_fin', 'heure_fermeture', 'sur_rdv', 'est_ferme']
    ordering = ['jour_semaine']


@admin.register(UserMensuration)
class UserMensurationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'is_main', 'user']
    list_filter = ['is_main']
    ordering = ['ref_user__email', 'is_main']

    def user(self, obj):
        return obj.ref_user.email


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ['id', 'rayon', 'section', 'type_produit']
    list_filter = ['ref_rayon__rayon', 'ref_section__section', 'ref_type_produit__type_produit']
    ordering = ['ref_rayon__rayon', 'ref_section__section', 'ref_type_produit__type_produit']

    def rayon(self, obj):
        return obj.ref_rayon.rayon

    def section(self, obj):
        return obj.ref_section.section

    def type_produit(self, obj):
        return obj.ref_type_produit.type_produit


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
    list_display = ['id', 'rue', 'numero', 'boite', 'ville', 'user']

    def ville(self, obj):
        return obj.ref_ville.ville

    def user(self, obj):
        return obj.ref_user.email


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ['ville', 'code_postale']
    ordering = ['code_postale']
    search_fields = ['ville', 'code_postale']


models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
