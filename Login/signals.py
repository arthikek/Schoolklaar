import datetime
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from Login.models import Materiaal, LeerlingVakRating, LeerlingVakRatingHistory
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
    Deletes old file from filesystem when corresponding `Materiaal` object 
    is updated with new file and checks if the new file is saved.
    """
    print("Running pre_save receiver...")
    
    if not instance.pk:
        return False

    try:
        old_file = Materiaal.objects.get(pk=instance.pk).bestand
    except Materiaal.DoesNotExist:
        print("Error: Materiaal instance not found in the database.")
        return False

    new_file = instance.bestand
    if not old_file == new_file:
        print("New file detected...")
        
        # Delete old file
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
                print("Old file deleted.")
            else:
                print("Old file not found on the filesystem.")
        except Exception as e:
            print(f"Error deleting old file: {str(e)}")

        # Check if the new file is saved
        try:
            if new_file and os.path.isfile(new_file.path):
                print("New file is saved and exists on the filesystem.")
            else:
                print("New file is not saved or doesn't exist.")
        except Exception as e:
            print(f"Error checking new file: {str(e)}")
            raise ValidationError("There was an error checking the new file. Please ensure it's correctly uploaded.")


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
            

