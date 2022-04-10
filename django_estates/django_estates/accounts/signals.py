from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django_estates.accounts.models import Profile, DjangoEstatesUser


@receiver(post_save, sender=DjangoEstatesUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Users'))


@receiver(pre_save, sender=Profile)
def check_is_complete(sender, instance, **kwargs):
    if instance.first_name and instance.last_name \
            and instance.image and instance.description and instance.phone_number:
        instance.is_complete = True
