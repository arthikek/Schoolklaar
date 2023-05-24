from django.utils import timezone
from Login.models import Sessie

def strip_time_from_dates():
    for sessie in Sessie.objects.all():
        # Extract date part only from the datetime field
        date_only = sessie.datum.date()
        # Replace the existing datetime with the date only value
        sessie.datum = date_only
        sessie.save()

# Call the function to start the update process
strip_time_from_dates()