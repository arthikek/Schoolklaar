from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from Login.models import Materiaal
from django.dispatch import receiver
import os
from django.core.cache import cache
    
@receiver(post_delete, sender=Materiaal)
def delete_materiaal(sender, instance, **kwargs):
    # instance is the Materiaal object being deleted
    print('You have deleted a Materiaal')
    if instance.bestand:
        if os.path.isfile(instance.bestand.path):
            os.remove(instance.bestand.path)


@receiver(pre_save, sender=Materiaal)
def auto_check_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Materiaal` object is updated
    with new file.
    """
    print("Running pre_save receiver...")
    
    if not instance.pk:
        return False

    try:
        old_file = Materiaal.objects.get(pk=instance.pk).bestand
    except Materiaal.DoesNotExist:
        return False

    new_file = instance.bestand
    if not old_file == new_file:
        print("New file detected, deleting old file...")
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            print("Old file deleted.")



@receiver(pre_save, sender=Materiaal)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding  Materiaal` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Materiaal.objects.get(pk=instance.pk).bestand
    except Materiaal.DoesNotExist:
        return False

    new_file = instance.bestand
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)