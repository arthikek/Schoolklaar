from datetime import datetime
from django.utils import timezone
from Login.models import Leerling, Sessie, Begeleider, User, Vak, Klas, Niveau, School
from random import randint  # Import randint

# Assuming you have already retrieved the Leerling instance for "Sam Aalders"
leerling = Leerling.objects.get(naam="sam")
begeleider_test=User.objects.get(username='Iris')
school_test=School.objects.get(naam='vo')

# Create 20 sessions for Sam Aalders
for i in range(1, 21):
    # Create a new Sessie instance
    sessie = Sessie.objects.create(
        datum=timezone.now(),  # Use the current datetime as the session date
        inzicht=randint(1, 5),  # Set a random inzicht value for each session
        kennis=randint(1, 5),  # Set a random kennis value for each session
        werkhouding=randint(1, 5),  # Set a random werkhouding value for each session
        extra="Some text here",
        Leerling=leerling,  # Assign the session to Sam Aalders
        begeleider=begeleider_test,
        school=school_test,
        vak=Vak.objects.get(naam='Frans'),
    )
    # Save the session
    sessie.save()

print("Sessions created successfully.")
