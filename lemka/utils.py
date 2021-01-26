import os

from lemka_api.utils import Utils


def ajout_du_slug(instance, slug):
    Class = instance.__class__
    if Class.objects.filter(slug=slug).exists():
        random_string = Utils.generate_random_string()
        instance.slug = slug + "-" + random_string
    else:
        instance.slug = slug


def path_and_rename_user_image(instance, filename):
    upload_to = ''
    ext = filename.split('.')[-1]
    # get filename
    if instance.username:
        user = instance.username
        dossier = 'profile_pics'
        upload_to = f'{dossier}/{user}'
        filename = f'{user}-{Utils.generate_random_string()}.{ext}'
    else:
        # set filename as random string
        filename = f'{Utils.generate_random_string()}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename_article_image(instance, filename):
    upload_to = ''
    ext = filename.split('.')[-1]
    if instance.ref_article.slug:
        article = instance.ref_article.slug
        dossier = 'articles'
        upload_to = f'{dossier}/{article}'
        filename = f'{article}-{Utils.generate_random_string()}.{ext}'
    else:
        # set filename as random string
        filename = f'{Utils.generate_random_string()}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename_mercerie_couleur_image(instance, filename):
    upload_to = ''
    ext = filename.split('.')[-1]
    if instance.ref_mercerie_couleur.ref_mercerie.reference:
        dossier = 'mercerie'
        mercerie = instance.ref_mercerie_couleur.ref_mercerie.reference
        couleur = instance.ref_mercerie_couleur.ref_couleur.nom
        upload_to = f'{dossier}/{mercerie}'
        filename = f'{mercerie}-{couleur}-{Utils.generate_random_string()}.{ext}'
    else:
        # set filename as random string
        filename = f'{Utils.generate_random_string()}.{ext}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)
