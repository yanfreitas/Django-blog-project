from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profiles


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create a profile to a created user"""
    if created:
        Profiles.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the profile when the user is saved"""
    instance.profiles.save()
