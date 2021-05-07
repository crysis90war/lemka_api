from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from lemka.models import UserMensuration, Mensuration, UserMesure


@receiver(pre_save, sender=UserMensuration)
def pre_save_user_mensuration(sender, instance, *args, **kwargs):
    if instance and instance.is_main is True:
        if UserMensuration.objects.filter(ref_user=instance.ref_user, is_main=True).exists():
            user_mensurations = UserMensuration.objects.filter(ref_user=instance.ref_user, is_main=True)
            for user_mensuration in user_mensurations:
                user_mensuration.is_main = False
                user_mensuration.save()


@receiver(post_save, sender=UserMensuration)
def create_user_mensuration(sender, instance, created, **kwargs):
    if created:
        mensurations = Mensuration.objects.all()

        for mensuration in mensurations:
            UserMesure.objects.create(ref_mensuration=mensuration, ref_user_mensuration=instance)


@receiver(post_delete, sender=UserMensuration)
def update_user_mensuration_after_delete(sender, instance, *args, **kwargs):
    if sender == UserMensuration:
        if UserMensuration.objects.filter(ref_user=instance.ref_user, is_main=True).exists():
            pass
        else:
            user_mensuration = UserMensuration.objects.filter(ref_user=instance.ref_user, is_main=False).first()
            if user_mensuration:
                user_mensuration.is_main = True
                user_mensuration.save()
            else:
                pass

"""
Faire la même pour pre-save adresse (is_main)
"""