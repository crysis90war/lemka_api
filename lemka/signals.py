import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from lemka.models import *
from lemka.utils import ajout_du_slug


@receiver(pre_save, sender=Article)
def ajouter_slug_article(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.titre)
        ajout_du_slug(instance, slug)


@receiver(pre_save, sender=DemandeDevis)
def ajout_numero_demande_devis(sender, instance, *args, **kwargs):
    if instance and not instance.numero_demande_devis:
        date = datetime.datetime.now().strftime ("%Y%m%d")
        numero_demande_devis = date + Utils.generate_random_numbers()
        instance.numero_demande_devis = numero_demande_devis


@receiver(pre_save, sender=Devis)
def ajout_numero_devis(sender, instance, *args, **kwargs):
    if instance and not instance.numero_devis:
        date = datetime.datetime.now().strftime ("%Y%m%d")
        numero_devis = date + Utils.generate_random_numbers()
        instance.numero_devis = numero_devis


@receiver(pre_save, sender=ArticleImage)
def article_image_is_main(sender, instance, *args, **kwargs):
    if instance:
        a_i_is_main_true = ArticleImage.objects.filter(ref_article__slug=instance.ref_article.slug, is_main=True).exists()
        a_i_is_main_false = ArticleImage.objects.filter(ref_article__slug=instance.ref_article.slug, is_main=False).exists()
        if instance.is_main is True:
            if a_i_is_main_true:
                article_images = ArticleImage.objects.filter(ref_article__slug=instance.ref_article.slug, is_main=True)
                for article_image in article_images:
                    article_image.is_main = False
                    article_image.save()
        elif instance.is_main is False:
            article_true_count = ArticleImage.objects.filter(ref_article__slug=instance.ref_article.slug, is_main=True).count()
            print(article_true_count)
            if not a_i_is_main_true and a_i_is_main_false:
                article_image = ArticleImage.objects.filter(ref_article__slug=instance.ref_article.slug, is_main=False).first()
                article_image.is_main = True
                article_image.save()
            if not a_i_is_main_true and not a_i_is_main_false:
                instance.is_main = True
                instance.save()


# @receiver(pre_save, sender=Rayon)
# def ajout_rayon_slug(sender, instance, *args, **kwargs):
#     if instance and not instance.rayon_slug:
#         rayon_slug = slugify(instance.rayon)
#         if Rayon.objects.filter(rayon_slug=rayon_slug).exists():
#             random_string = Utils.generate_random_string()
#             instance.rayon_slug = rayon_slug + "-" + random_string
#         else:
#             instance.rayon_slug = rayon_slug
#
#
# @receiver(pre_save, sender=Section)
# def ajout_section_slug(sender, instance, *args, **kwargs):
#     if instance and not instance.section_slug:
#         section_slug = slugify(instance.section)
#         if Section.objects.filter(section_slug=section_slug).exists():
#             random_string = Utils.generate_random_string()
#             instance.section_slug = section_slug + "-" + random_string
#         else:
#             instance.section_slug = section_slug
#
#
# @receiver(pre_save, sender=TypeProduit)
# def ajout_type_produit_slug(sender, instance, *args, **kwargs):
#     if instance and not instance.type_produit_slug:
#         type_produit_slug = slugify(instance.type_produit)
#         if TypeProduit.objects.filter(type_produit_slug=type_produit_slug).exists():
#             random_string = Utils.generate_random_string()
#             instance.type_produit_slug = type_produit_slug + "-" + random_string
#         else:
#             instance.type_produit_slug = type_produit_slug
#
#
# @receiver(pre_save, sender=Tag)
# def ajout_tag_slug(sender, instance, *args, **kwargs):
#     if instance and not instance.tag_slug:
#         tag_slug = slugify(instance.tag)
#         if Tag.objects.filter(tag_slug=tag_slug).exists():
#             random_string = Utils.generate_random_string()
#             instance.tag_slug = tag_slug + "-" + random_string
#         else:
#             instance.tag_slug = tag_slug
#
#
# @receiver(pre_save, sender=Categorie)
# def ajout_categorie_slug(sender, instance, *args, **kwargs):
#     if instance and not instance.slug:
#         categorie_slug = slugify(instance.nom)
#         if Categorie.objects.filter(slug=categorie_slug).exists():
#             random_string = Utils.generate_random_string()
#             instance.slug = categorie_slug + "-" + random_string
#         else:
#             instance.slug = categorie_slug
