from datetime import datetime
from turtle import mode
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

class Employer(models.Model):
    naam = models.CharField(max_length=50)
    achternaam = models.CharField(max_length=50)
    email = models.EmailField()
   

    def __str__(self):
        return f'{self.naam} {self.achternaam}'

    def get_absolute_url(self):
        return reverse('Employer_detail', kwargs={'pk': self.pk})
    
class School(models.Model):
    naam = models.CharField(max_length=30)
    grootte = models.IntegerField()    
    def __str__(self) -> str:
        return f'{self.naam}'

class Leerling(models.Model):
    naam = models.CharField(max_length=30)
    achternaam = models.CharField(max_length=30)
    email = models.EmailField()
    school = models.ForeignKey(School, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f'{self.naam} {self.achternaam}'

    def get_absolute_url(self):
        return reverse('Leerling_detail', kwargs={'pk': self.pk})




class Sessie(models.Model):
    Leerling = models.ForeignKey(Leerling, on_delete=models.CASCADE)
    begeleider = models.ForeignKey(Employer, null=True, on_delete=models.SET_NULL)
    inzicht = models.IntegerField()
    kennis = models.IntegerField()
    werkhouding = models.IntegerField()
    extra = models.TextField()
    datum = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Sessie {self.pk} ({self.Leerling}, {self.begeleider})'

    def get_absolute_url(self):
        return reverse('Sessie_detail', kwargs={'pk': self.pk})
    


