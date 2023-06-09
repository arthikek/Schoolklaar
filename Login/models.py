from datetime import datetime
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



class School(models.Model):
    naam = models.CharField(max_length=30)
    grootte = models.IntegerField()

    def __str__(self) -> str:
        return self.naam


class Niveau(models.Model):
    naam = models.CharField(max_length=50)
    scholen = models.ManyToManyField(School, related_name='niveaus')

    def __str__(self):
        return self.naam


class Vak(models.Model):
    naam = models.CharField(max_length=50)
    niveaus = models.ManyToManyField(Niveau, related_name='vakken')
    
    def __str__(self):
        return self.naam


class Klas(models.Model):
    naam = models.IntegerField()
    niveaus = models.ManyToManyField(Niveau, related_name='klassen')
    vakken = models.ManyToManyField(Vak, related_name='klassen')

    def __str__(self):
        return str(self.naam)



class Begeleider(models.Model):
    gebruiker = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    scholen = models.ManyToManyField(School, related_name='begeleiders')

    def __str__(self) -> str:
        return str(self.gebruiker)


class Teamleider(models.Model):
    gebruiker = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.gebruiker)


class Leerling(models.Model):
    naam = models.CharField(max_length=30)
    achternaam = models.CharField(max_length=30) # type: ignore
    email = models.EmailField()
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE)
    klas = models.ForeignKey(Klas, null=True, on_delete=models.SET_NULL)
    niveau = models.ForeignKey(Niveau, null=True, on_delete=models.SET_NULL)
    
    
    def __str__(self):
        return f'{self.naam} {self.achternaam}'

    def get_absolute_url(self):
        return reverse('Leerling_detail', kwargs={'pk': self.pk})
    
    
class Materiaal(models.Model):
    titel = models.CharField(max_length=100)
    bestand = models.FileField(upload_to='materialen/')
    vak = models.ForeignKey(Vak, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    klas = models.ForeignKey(Klas, on_delete=models.CASCADE)
    omschrijving = models.TextField(default='Schrijf de beschrijvingen zo uitgebreid mogelijk. We gaan dit later verwerken in een zoeksysteem')
    leerling = models.ForeignKey(
        Leerling, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='persoonlijk_materiaal'
    )
    # null and blank are set to True w
       
           
class Sessie(models.Model):
    INZICHT_CHOICES = [(i, str(i)) for i in range(1, 6)]
    KENNIS_CHOICES = [(i, str(i)) for i in range(1, 6)]
    WERKHOUDING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    Leerling = models.ForeignKey(Leerling, on_delete=models.CASCADE)
    begeleider = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    inzicht = models.IntegerField(choices=INZICHT_CHOICES)
    kennis = models.IntegerField(choices=KENNIS_CHOICES)
    werkhouding = models.IntegerField(choices=WERKHOUDING_CHOICES)
    extra = models.TextField()
    datum = models.DateField(default=datetime.now)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    vak = models.ForeignKey(Vak, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Sessie {self.pk} ({self.Leerling}, {self.begeleider})' 

    def get_absolute_url(self):
        return reverse('Sessie_detail', kwargs={'pk': self.pk})

