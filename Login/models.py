import datetime
from distutils.command import sdist
from turtle import mode
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.db import models
from pkg_resources import DistInfoDistribution
from rest_framework.views import APIView
from django.db.models import Q
from django.utils.crypto import get_random_string


import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Model representing a school
class School(models.Model):
    naam = models.CharField(max_length=30)  # Name of the school
    grootte = models.IntegerField()  # Size (number of students or other metric) of the school
    secret_code = models.CharField(max_length=6, default="f2AjB89")  # Secret code for registering students"  )
    def __str__(self) -> str:
        return self.naam

# Model representing an education level or grade
class Niveau(models.Model):
    naam = models.CharField(max_length=50)  # Name of the level or grade
    scholen = models.ManyToManyField(School, related_name='niveaus')  # Schools that have this level

    def __str__(self):
        return self.naam

# Model representing a subject or course
class Vak(models.Model):
    naam = models.CharField(max_length=50)  # Name of the subject
    niveaus = models.ManyToManyField(Niveau, related_name='vakken')  # Levels that have this subject
    
    def __str__(self):
        return self.naam

# Model representing a class in a school
class Klas(models.Model):
    naam = models.IntegerField()  # Class identifier or name
    niveaus = models.ManyToManyField(Niveau, related_name='klassen')  # Levels associated with this class
    vakken = models.ManyToManyField(Vak, related_name='klassen')  # Subjects taught in this class

    def __str__(self):
        return str(self.naam)

# Model representing a mentor or tutor
class Begeleider(models.Model):
    gebruiker = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)  # User account of the mentor
    scholen = models.ManyToManyField(School, related_name='begeleiders')  # Schools the mentor is associated with

    def __str__(self) -> str:
        return str(self.gebruiker)

# Model representing a team leader
class Teamleider(models.Model):
    gebruiker = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)  # User account of the team leader
    school = models.ForeignKey(School, on_delete=models.CASCADE)  # School the team leader belongs to

    def __str__(self) -> str:
        return str(self.gebruiker)

# Model representing a student
class Leerling(models.Model):
    # Student's basic details
    naam = models.CharField(max_length=30)
    achternaam = models.CharField(max_length=30)
    email = models.EmailField()
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE)
    klas = models.ForeignKey(Klas, null=True, on_delete=models.SET_NULL)
    niveau = models.ForeignKey(Niveau, null=True, on_delete=models.SET_NULL)
    gebruiker = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    vakken = models.ManyToManyField(Vak, through='LeerlingVakRating', related_name='leerlingen')  # Subjects the student is enrolled in
    
    def __str__(self):
        return f'{self.naam} {self.achternaam}'

    def get_absolute_url(self):
        return reverse('Leerling_detail', kwargs={'pk': self.pk})

# Model for storing student's rating or feedback for a particular subject
class LeerlingVakRating(models.Model):
    MOEILIJKHEIDSKEUZES = [(i, str(i)) for i in range(1, 11)]  # Choices for difficulty ratings
    leerling = models.ForeignKey(Leerling, on_delete=models.CASCADE)
    vak = models.ForeignKey(Vak, on_delete=models.CASCADE)
    cijfer = models.IntegerField(choices=MOEILIJKHEIDSKEUZES, default=5)  # Numeric rating for difficulty
    beschrijving = models.TextField(default='Schrijf hier een beschrijving van het vak')  # Description or feedback

    class Meta:
        unique_together = ['leerling', 'vak']  # Ensure a unique rating for each subject per student

class LeerlingVakRatingHistory(models.Model):
    leerling_vak_rating = models.ForeignKey(LeerlingVakRating, on_delete=models.CASCADE)
    cijfer = models.IntegerField(default=5)
    beschrijving = models.TextField()
    date_recorded = models.DateField(auto_now_add=True)
    
    def vak_name(self):
        return self.leerling_vak_rating.vak.naam
    vak_name.short_description = "Vak Name"
# Model representing learning materials
class Materiaal(models.Model):
    # Material details
    titel = models.CharField(max_length=100)
    bestand = models.FileField(upload_to='materialen/')
    vak = models.ForeignKey(Vak, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    klas = models.ForeignKey(Klas, on_delete=models.CASCADE)
    omschrijving = models.TextField(default='Schrijf de beschrijvingen zo uitgebreid mogelijk. We gaan dit later verwerken in een zoeksysteem')  # Description of the material
    leerling = models.ForeignKey(Leerling, null=True, blank=True, on_delete=models.SET_NULL, related_name='persoonlijk_materiaal')  # If the material is specific to a student

# Model representing a session between a student and a mentor/tutor
class Sessie(models.Model):
    # Choices for different ratings
    INZICHT_CHOICES = [(i, str(i)) for i in range(1, 6)]
    KENNIS_CHOICES = [(i, str(i)) for i in range(1, 6)]
    WERKHOUDING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    # Session details
    Leerling = models.ForeignKey(Leerling, on_delete=models.CASCADE)
    begeleider = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)  # Tutor/mentor for the session
    inzicht = models.IntegerField(choices=INZICHT_CHOICES)  # Insight rating
    kennis = models.IntegerField(choices=KENNIS_CHOICES)  # Knowledge rating
    werkhouding = models.IntegerField(choices=WERKHOUDING_CHOICES)  # Work attitude rating
    extra = models.TextField()  # Additional notes
    datum = models.DateField(default=datetime.date.today())  # Date of the session
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    vak = models.ForeignKey(Vak, null=True, on_delete=models.SET_NULL)  # Subject of the session

    def __str__(self):
        return f'Sessie {self.pk} ({self.Leerling}, {self.begeleider})' 

    def get_absolute_url(self):
        return reverse('Sessie_detail', kwargs={'pk': self.pk})
