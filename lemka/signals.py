import datetime

from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from rest_framework.generics import get_object_or_404

from lemka.models import *
from lemka.utils import ajout_du_slug


@receiver(pre_save, sender=Article)
def ajouter_slug_article(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.titre)
        ajout_du_slug(instance, slug)


@receiver(pre_save, sender=Mercerie)
def ajouter_reference_mercerie(sender, instance, *args, **kwargs):
    if instance and not instance.reference:
        string = 'MERC'
        date = datetime.datetime.now().strftime("%Y%m%d")
        random = Utils.generate_random_numbers()
        reference = string + date + random
        instance.reference = reference


@receiver(pre_save, sender=DemandeDevis)
def ajout_numero_demande_devis(sender, instance, *args, **kwargs):
    if instance and not instance.numero_demande_devis:
        date = datetime.datetime.now().strftime("%Y%m%d")
        numero_demande_devis = date + Utils.generate_random_numbers()
        instance.numero_demande_devis = numero_demande_devis


@receiver(pre_save, sender=Devis)
def ajout_numero_devis(sender, instance, *args, **kwargs):
    if instance and not instance.numero_devis:
        date = datetime.datetime.now().strftime("%Y%m%d")
        numero_devis = date + Utils.generate_random_numbers()
        instance.numero_devis = numero_devis


@receiver(pre_save, sender=ArticleImage)
def article_main_image(sender, instance, *args, **kwargs):
    if instance:
        if ArticleImage.objects.filter(ref_article=instance.ref_article).exists():
            if instance.is_main is True:
                if ArticleImage.objects.filter(ref_article=instance.ref_article, is_main=True).exists():
                    instance.is_main = False
        else:
            if instance.is_main is False:
                instance.is_main = True


@receiver(post_delete, sender=ArticleImage)
def article_image_delete(sender, instance, *args, **kwargs):
    if instance:
        if ArticleImage.objects.filter(ref_article=instance.ref_article).exists():
            if ArticleImage.objects.filter(ref_article=instance.ref_article, is_main=True).exists():
                pass
            else:
                article_image = ArticleImage.objects.filter(ref_article=instance.ref_article, is_main=False).first()
                article_image.is_main = True
                article_image.save()


@receiver(pre_save, sender=MercerieImage)
def mercerie_main_image(sender, instance, *args, **kwargs):
    if instance:
        if MercerieImage.objects.filter(ref_mercerie=instance.ref_mercerie).exists():
            if instance.is_main is True:
                if MercerieImage.objects.filter(ref_mercerie=instance.ref_mercerie, is_main=True).exists():
                    instance.is_main = False
        else:
            if instance.is_main is False:
                instance.is_main = True


@receiver(post_delete, sender=MercerieImage)
def mercerie_image_delete(sender, instance, *args, **kwargs):
    if instance:
        if MercerieImage.objects.filter(ref_mercerie=instance.ref_mercerie).exists():
            if MercerieImage.objects.filter(ref_mercerie=instance.ref_mercerie, is_main=True).exists():
                pass
            else:
                mercerie_image = MercerieImage.objects.filter(ref_mercerie=instance.ref_mercerie, is_main=False).first()
                mercerie_image.is_main = True
                mercerie_image.save()


@receiver(post_save, sender=Devis)
def demande_devis_traite(sender, instance, *args, **kwargs):
    if instance and instance.est_soumis is True:
        demande_devis = get_object_or_404(DemandeDevis, pk=instance.ref_demande_devis.id)
        demande_devis.est_traite = True
        demande_devis.save()


@receiver(post_save, sender=Mensuration)
def mensuration_user_mensuration(sender, instance, *args, **kwargs):
    if instance:
        user_mensuration = UserMesure.objects.values('ref_user_mensuration').distinct()
        for mesure in list(user_mensuration):
            if not UserMesure.objects.filter(ref_user_mensuration_id=mesure['ref_user_mensuration'], ref_mensuration_id=instance.id).exists():
                UserMesure.objects.create(ref_user_mensuration_id=mesure['ref_user_mensuration'], ref_mensuration_id=instance.id)

# def user_mensuration(sender, instance, *arg, **kwargs):
#     if instance and instance.is_main is False:
#         user_mensuration = get_object_or_404(UserMensuration, pk=instance.id)

