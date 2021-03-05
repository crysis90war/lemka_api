import locale

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from lemka.manager import UserManager
from lemka.utils import *

locale.setlocale(locale.LC_TIME, '')
AUTH_PROVIDERS = {'facebook': 'facebook',
                  'google': 'google',
                  'twitter': 'twitter',
                  'email': 'email'}


class Genre(models.Model):
    genre = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.genre}'


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='Nom public')
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename_user_image)
    first_name = models.CharField(max_length=255, blank=True, null=False, default='', verbose_name='Prénom')
    last_name = models.CharField(max_length=255, blank=True, null=False, default='', verbose_name='Nom')
    numero_tel = models.CharField(max_length=255, blank=True, null=False, default='', verbose_name='Numéro tel.')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    ref_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Sexe')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.id} | {self.email}'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        self.username = self.username.lower()
        self.email = self.email.lower()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class AccompteDemande(models.Model):
    taux = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def __str__(self):
        taux = self.taux * 100
        return f'{taux} %'


class Pays(models.Model):
    pays = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pays}'


class Ville(models.Model):
    ref_pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    ville = models.CharField(max_length=255)
    code_postale = models.CharField(max_length=255)

    class Meta:
        ordering = ['ville']

    def __str__(self):
        return f'{self.ville} {self.code_postale}'


class Adresse(models.Model):
    rue = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    boite = models.CharField(max_length=255, blank=True)

    ref_ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    ref_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adresses')

    class Meta:
        ordering = ['ref_user__email', 'ref_ville__ville']

    def __str__(self):
        return f'{self.id} | {self.ref_user.email} {self.ref_ville.ville}'


class Mensuration(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class UserMensuration(models.Model):
    titre = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)

    ref_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensurations')

    class Meta:
        ordering = ['ref_user__username', '-is_main', 'titre']

    def __str__(self):
        if self.is_main is True:
            return f'{self.ref_user.username} - Principale | {self.titre}'
        else:
            return f'{self.ref_user.username} - Secondaire | {self.titre}'


class MensurationUserMensuration(models.Model):
    mesure = models.FloatField(default=0.0, validators=[MinValueValidator(0.00), MaxValueValidator(260.00)])

    ref_user_mensuration = models.ForeignKey(UserMensuration, on_delete=models.CASCADE)
    ref_mensuration = models.ForeignKey(Mensuration, on_delete=models.CASCADE, related_name='Mensuration')

    class Meta:
        ordering = ['ref_user_mensuration__ref_user__username', '-ref_user_mensuration__is_main']

    def __str__(self):
        return f'{self.ref_user_mensuration.ref_user.username} | {self.ref_user_mensuration.titre} - {self.ref_mensuration.nom} - {self.mesure} cm'


class Rayon(models.Model):
    rayon = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.rayon}'


class Section(models.Model):
    section = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['section']

    def __str__(self):
        return f'{self.section}'


class TypeProduit(models.Model):
    type_produit = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['type_produit']

    def __str__(self):
        return self.type_produit


class Catalogue(models.Model):
    ref_rayon = models.ForeignKey(Rayon, on_delete=models.CASCADE)
    ref_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    ref_type_produit = models.ForeignKey(TypeProduit, on_delete=models.CASCADE)

    class Meta:
        ordering = ['ref_rayon', 'ref_section', 'ref_type_produit']

    def __str__(self):
        return f'{self.id} - {self.ref_rayon} - {self.ref_section} - {self.ref_type_produit}'


class TypeService(models.Model):
    type_service = models.CharField(max_length=255, unique=True, null=False, blank=False)
    duree_minute = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(180)], blank=False,
                                               null=False)

    def __str__(self):
        return f'{self.type_service} - {self.duree_minute}'


class Tag(models.Model):
    tag = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        return f'{self.id} {self.tag}'


class Article(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()

    slug = models.SlugField(max_length=255, unique=True, null=False, blank=True, editable=False)
    est_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ref_type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE)
    ref_catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE, default=None)

    ref_tag = models.ManyToManyField(Tag, blank=True, related_name='tags')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return f'{self.titre}'


class ArticleImage(models.Model):
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename_article_image)
    is_main = models.BooleanField(default=False)

    ref_article = models.ForeignKey(Article, on_delete=models.Model)

    class Meta:
        ordering = ['ref_article__slug', '-is_main']

    def save(self, *args, **kwargs):
        super(ArticleImage, self).save(*args, **kwargs)

        # if self.image:
        #     Utils.resize_image(self.image.path, (720, 1008))

    def __str__(self):
        if self.is_main is True:
            return f'Principale - {self.ref_article.slug}'
        else:
            return f'Secondaire - {self.ref_article.slug}'


class Categorie(models.Model):
    nom = models.CharField(max_length=255, null=False, blank=True, unique=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f'{self.nom}'


class Couleur(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nom}'


class Mercerie(models.Model):
    nom = models.CharField(max_length=255)
    est_publie = models.BooleanField(default=False)

    ref_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nom}'


class MercerieOption(models.Model):
    reference = models.CharField(max_length=255)
    est_publie = models.BooleanField(default=False)
    description = models.TextField(default="")
    prix_u_ht = models.DecimalField(max_digits=10, decimal_places=2,
                                    validators=[MinValueValidator(0.00), MaxValueValidator(999999999.99)])
    stock = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(999999.9)])

    ref_mercerie = models.ForeignKey(Mercerie, on_delete=models.CASCADE)
    ref_couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE)

    class Meta:
        ordering = ['ref_mercerie__nom', 'ref_couleur__nom']

    def __str__(self):
        return f'{self.reference} | {self.ref_mercerie.nom} - {self.ref_couleur.nom}'


class Dimension(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class MercerieOptionDimension(models.Model):
    ref_mercerie_option = models.ForeignKey(MercerieOption, null=False, blank=False, on_delete=models.CASCADE)
    ref_dimension = models.ForeignKey(Dimension, null=False, blank=False, on_delete=models.CASCADE)
    valeur = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(0.00), MaxValueValidator(999999999.99)])

    def __str__(self):
        return f'{self.ref_mercerie_option.ref_mercerie.nom} | {self.ref_dimension.nom} - {self.valeur} cm'


class MercerieOptionImage(models.Model):
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename_mercerie_couleur_image)
    is_main = models.BooleanField(default=False)

    ref_mercerie_option = models.ForeignKey(MercerieOption, on_delete=models.CASCADE)

    class Meta:
        ordering = ['ref_mercerie_option__ref_mercerie__nom', '-is_main']

    def save(self, *args, **kwargs):
        super(MercerieOptionImage, self).save(*args, **kwargs)

        # if self.image:
        #     Utils.resize_image(self.image.path, (720, 720))

    def __str__(self):
        reference = self.ref_mercerie_option.reference
        nom = self.ref_mercerie_option.ref_mercerie.nom
        couleur = self.ref_mercerie_option.ref_couleur.nom
        if self.is_main is True:
            return f'{reference} | {nom} {couleur} - Principale'
        else:
            return f'{reference} | {nom} {couleur} - Secondaire'


# class Materiel(Commun):
#     reference = models.CharField(max_length=255)
#     prix_u_ht = models.DecimalField(max_digits=10, decimal_places=3)
#     stock = models.FloatField()
#
#     def __str__(self):
#         return f'{self.reference} | {self.nom}'
#
#
# class Tissu(Commun):
#     reference = models.CharField(max_length=255)
#     densite = models.FloatField()
#
#     def __str__(self):
#         return f'{self.nom}'
#
#
# class TissuCouleur(models.Model):
#     prix_u_ht = models.DecimalField(max_digits=10, decimal_places=3)
#     stock = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(999999.9)])
#
#     ref_tissu = models.ForeignKey(Tissu, on_delete=models.CASCADE)
#     ref_couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE)
#
#     def __str__(self):
#         reference = self.ref_tissu.reference
#         couleur = self.ref_couleur.nom
#         return f'{couleur} | {reference}'
#
#
# class TissuCouleurImage(models.Model):
#     image = models.ImageField(default='default.jpg', upload_to=path_and_rename_tissu_couleur_image)
#     is_main = models.BooleanField(default=False)
#
#     ref_tissu_couleur = models.ForeignKey(TissuCouleur, on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ['ref_tissu_couleur__ref_tissu__nom', '-is_main']
#
#     def save(self, *args, **kwargs):
#         super(TissuCouleurImage, self).save(*args, **kwargs)
#
#         if self.image:
#             resize_image(self.image.path, (360, 360))
#
#     def __str__(self):
#         reference = self.ref_tissu_couleur.ref_tissu.reference
#         couleur = self.ref_tissu_couleur.ref_couleur.nom
#         if self.is_main is True:
#             return f'{reference} | {couleur} - Principale'
#         else:
#             return f'{reference} | {couleur} - Secondaire'


class DemandeDevis(models.Model):
    numero_demande_devis = models.PositiveIntegerField(unique=True)
    titre = models.CharField(max_length=255)
    remarque = models.TextField()
    est_urgent = models.BooleanField(default=False)
    est_soumis = models.BooleanField(default=False)
    est_traite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    ref_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE)
    ref_catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)

    ref_mensuration = models.ManyToManyField(UserMensuration, blank=True)
    # ref_materiel = models.ManyToManyField(Materiel, blank=True, related_name='matérieux')
    # ref_tissu = models.ManyToManyField(TissuCouleur, blank=True, related_name='tissus')
    ref_mercerie_option = models.ManyToManyField(MercerieOption, blank=True, related_name='merceries')
    ref_article = models.ManyToManyField(Article, blank=True, related_name='articles')

    class Meta:
        ordering = ['-est_soumis', '-created_at']

    def __str__(self):
        numero = self.numero_demande_devis
        email = self.ref_user.email
        titre = self.titre
        date = self.created_at.strftime("%D %H:%M:%S")
        if self.est_soumis is True:
            return f'[V] {numero} | {email} - {titre} ({date})'
        else:
            return f'[X] {numero} | {email} - {titre} ({date})'


class DemadeDevisImage(models.Model):
    image = models.ImageField()

    ref_demande_devis = models.ForeignKey(DemandeDevis, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ref_demande_devis.ref_user.email} - {self.ref_demande_devis.titre}'


class Devis(models.Model):
    numero_devis = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    remarque = models.TextField()
    est_accepte = models.BooleanField(null=True, blank=True)
    est_soumis = models.BooleanField(default=False)

    ref_accompte = models.ForeignKey(AccompteDemande, on_delete=models.CASCADE, verbose_name='Accompte démandé')
    ref_demande_devis = models.ForeignKey(DemandeDevis, null=True, blank=True, on_delete=models.CASCADE,
                                          verbose_name='Demande de devis')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        email = self.ref_demande_devis.ref_user.email
        date = self.created_at
        devis = self.numero_devis
        return f'{devis} | {email} ({date})'


class Discussion(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    est_vue = models.BooleanField(default=False)

    ref_devis = models.ForeignKey(Devis, on_delete=models.CASCADE)
    ref_user_envoyeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_envoyeur')
    ref_user_receveur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_receveur')

    class Meta:
        ordering = ['ref_devis__numero_devis', '-created_at']

    def __str__(self):
        devis = self.ref_devis.numero_devis
        envoyeur = self.ref_user_envoyeur.username
        receveur = self.ref_user_receveur.username
        date = self.created_at.strftime("%D %M %Y %H:%M:%S")
        return f'{devis} | {envoyeur} -> {receveur} ({date})'


class BonCommande(models.Model):
    numero_bon_commande = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    accompte_paye = models.BooleanField()

    ref_devis = models.ForeignKey(Devis, on_delete=models.CASCADE)


class Tva(models.Model):
    taux = models.FloatField(unique=True)

    class Meta:
        ordering = ['taux']

    def __str__(self):
        taux_en_pct = self.taux * 100
        return f'{taux_en_pct} %'


class Facture(models.Model):
    numero_facture = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    ref_bon_commande = models.ForeignKey(BonCommande, on_delete=models.CASCADE)

    """
    Calcules:
    --------

    Total HT + TVA - Accompte = Total TTC
    
    """


class Detail(models.Model):
    designation = models.CharField(max_length=255)
    prix_u_ht = models.DecimalField(max_digits=10, decimal_places=3)
    quantite = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(999999999.0)])

    ref_devis = models.ForeignKey(Devis, on_delete=models.CASCADE)
    ref_tva = models.ForeignKey(Tva, on_delete=models.CASCADE)

    def __str__(self):
        email = self.ref_devis.ref_demande_devis.ref_user.email
        numero_devis = self.ref_devis.numero_devis
        date = self.ref_devis.created_at
        return f'{numero_devis} | {email} - {date}'


class EntrepriseLemka(models.Model):
    nom_societe = models.CharField(max_length=255)
    rue = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    numero_tva = models.CharField(max_length=255)
    mail_contact = models.EmailField()
    numero_tel = models.CharField(max_length=255)
    site_web = models.CharField(max_length=255)

    ref_ville = models.ForeignKey(Ville, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nom_societe}'


class Horaire(models.Model):
    jour = models.CharField(max_length=255)
    jour_semaine = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(7)])
    heure_ouverture = models.TimeField(blank=True, null=True)
    pause_debut = models.TimeField(blank=True, null=True)
    pause_fin = models.TimeField(blank=True, null=True)
    heure_fermeture = models.TimeField(blank=True, null=True)
    sur_rdv = models.BooleanField()
    est_ferme = models.BooleanField()

    def __str__(self):
        if self.est_ferme:
            return f'{self.jour} | Fermé'
        elif self.sur_rdv:
            return f'{self.jour} | Sur Rendez-vous'
        else:
            ouverture = self.heure_ouverture.strftime("%H:%M")
            fermeture = self.heure_fermeture.strftime("%H:%M")
            return f'{self.jour} | De {ouverture} à {fermeture} heures'


class RendezVous(models.Model):
    date = models.DateField()
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    est_annule = models.BooleanField(default=0)

    ref_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    ref_type_service = models.ForeignKey(TypeService, null=False, blank=False, on_delete=models.CASCADE,
                                         verbose_name='Raison')

    ref_devis = models.ManyToManyField(Devis, blank=True, related_name='devis')

    def __str__(self):
        utilisateur = self.ref_user.username
        jour_rdv = self.date
        heure_rdv = self.start
        return f'{utilisateur} {jour_rdv} {heure_rdv}'
