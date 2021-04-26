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


class Tva(models.Model):
    taux = models.FloatField(unique=True)
    applicable = models.BooleanField(default=True)

    class Meta:
        ordering = ['taux']

    def __str__(self):
        taux_en_pct = self.taux * 100
        if self.applicable is True:
            return f'[V]{taux_en_pct} %'
        else:
            return f'[X]{taux_en_pct} %'


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename_user_image)
    first_name = models.CharField(max_length=255, blank=True, null=False, default='')
    last_name = models.CharField(max_length=255, blank=True, null=False, default='')
    numero_tel = models.CharField(max_length=255, blank=True, null=False, default='')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    ref_genre = models.ForeignKey(Genre, blank=True, null=True, on_delete=models.SET_NULL)

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
            return f'{self.pk} | {self.ref_user.username} - Principale | {self.titre}'
        else:
            return f'{self.pk} | {self.ref_user.username} - Secondaire | {self.titre}'


class UserMensurationMesure(models.Model):
    mesure = models.FloatField(default=0.0, validators=[MinValueValidator(0.00), MaxValueValidator(260.00)])

    ref_user_mensuration = models.ForeignKey(UserMensuration, on_delete=models.CASCADE)
    ref_mensuration = models.ForeignKey(Mensuration, on_delete=models.CASCADE, related_name='Mensuration')

    class Meta:
        ordering = ['ref_user_mensuration__ref_user__username', '-ref_user_mensuration__is_main', 'ref_mensuration__id']

    def __str__(self):
        username = self.ref_user_mensuration.ref_user.username
        titre = self.ref_user_mensuration.titre
        nom = self.ref_mensuration.nom
        mesure = self.mesure
        return f'{username} | {titre} - {nom} - {mesure} cm'


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

    ref_tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return f'{self.titre}'


class ArticleImage(models.Model):
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename_article_image)
    is_main = models.BooleanField(default=False)

    ref_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='imgs')

    class Meta:
        ordering = ['ref_article__slug', '-is_main']

    def save(self, *args, **kwargs):
        super(ArticleImage, self).save(*args, **kwargs)

    def __str__(self):
        if self.is_main is True:
            return f'Principale - {self.ref_article.slug}'
        else:
            return f'Secondaire - {self.ref_article.slug}'


class Categorie(models.Model):
    nom = models.CharField(max_length=255, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f'{self.nom}'


class Couleur(models.Model):
    nom = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return f'{self.nom}'


class Mercerie(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255, null=False, blank=False)
    est_publie = models.BooleanField(default=False)
    description = models.TextField(default="")
    prix_u_ht = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(999999999.99)])

    ref_tva = models.ForeignKey(Tva, on_delete=models.CASCADE, related_name='tva')
    ref_couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE)
    ref_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nom', 'ref_couleur__nom']

    def __str__(self):
        return f'{self.reference} | {self.nom} - {self.ref_couleur.nom}'


class Caracteristique(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class MercerieCaracteristique(models.Model):
    ref_mercerie = models.ForeignKey(Mercerie, null=False, blank=False, on_delete=models.CASCADE, related_name='catacteristiques')
    ref_caracteristique = models.ForeignKey(Caracteristique, null=False, blank=False, on_delete=models.CASCADE)
    valeur = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00), MaxValueValidator(999999999.99)])

    class Meta:
        ordering = ['ref_mercerie__nom']

    def __str__(self):
        return f'{self.ref_mercerie.nom} | {self.ref_caracteristique.nom} - {self.valeur}'


class MercerieImage(models.Model):
    image = models.ImageField(default='default.jpg', upload_to=path_and_rename_mercerie_image)
    is_main = models.BooleanField(default=False)

    ref_mercerie = models.ForeignKey(Mercerie, null=False, blank=False, on_delete=models.CASCADE, related_name='images')

    class Meta:
        ordering = ['ref_mercerie__nom', '-is_main']

    def save(self, *args, **kwargs):
        super(MercerieImage, self).save(*args, **kwargs)

        # if self.image:
        #     Utils.resize_image(self.image.path, (720, 720))

    def __str__(self):
        reference = self.ref_mercerie.reference
        nom = self.ref_mercerie.nom
        couleur = self.ref_mercerie.ref_couleur.nom
        if self.is_main is True:
            return f'{reference} | {nom} {couleur} - Principale'
        else:
            return f'{reference} | {nom} {couleur} - Secondaire'


class DemandeDevis(models.Model):
    numero_demande_devis = models.PositiveBigIntegerField(unique=True)
    titre = models.CharField(max_length=255)
    remarque = models.TextField()
    est_urgent = models.BooleanField(default=False)
    est_soumis = models.BooleanField(default=False)
    en_cours = models.BooleanField(default=False)
    est_traite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    ref_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE)
    ref_article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.SET_NULL)
    ref_mensuration = models.ForeignKey(UserMensuration, blank=True, null=True, on_delete=models.SET_NULL)

    ref_merceries = models.ManyToManyField(Mercerie, blank=True, related_name='merceries')

    class Meta:
        ordering = ['-created_at']

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
    image = models.ImageField(upload_to=path_and_rename_demande_devis_image)

    ref_demande_devis = models.ForeignKey(DemandeDevis, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ref_demande_devis.ref_user.email} - {self.ref_demande_devis.titre}'


class Devis(models.Model):
    numero_devis = models.PositiveBigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarque = models.TextField(default="", blank=True)
    est_accepte = models.BooleanField(null=True)
    est_soumis = models.BooleanField(default=False)

    ref_demande_devis = models.ForeignKey(DemandeDevis, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        email = self.ref_demande_devis.ref_user.email
        date = self.created_at
        devis = self.numero_devis
        return f'{devis} | {email} ({date})'


class Detail(models.Model):
    designation = models.CharField(max_length=255)
    prix_u_ht = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(999999999.0)])

    ref_devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name='details')
    ref_tva = models.ForeignKey(Tva, on_delete=models.CASCADE)

    def __str__(self):
        email = self.ref_devis.ref_demande_devis.ref_user.email
        numero_devis = self.ref_devis.numero_devis
        demande_devis_titre = self.ref_devis.ref_demande_devis.titre
        return f'{numero_devis} | {email} - {demande_devis_titre}'


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
    est_annule = models.BooleanField(default=False)

    ref_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    ref_type_service = models.ForeignKey(TypeService, null=False, blank=False, on_delete=models.CASCADE, verbose_name='service')

    ref_devis = models.ForeignKey(Devis, null=True, blank=True, on_delete=models.SET_NULL, related_name='devis')

    def __str__(self):
        utilisateur = self.ref_user.username
        jour_rdv = self.date
        heure_rdv = self.start
        return f'{utilisateur} {jour_rdv} {heure_rdv}'
