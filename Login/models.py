from datetime import datetime
from django.db import models
from django.shortcuts import reverse


class Employer(models.Model):
    naam = models.CharField(max_length=50)
    achternaam = models.CharField(max_length=50)
    email = models.EmailField()
   

    def __str__(self):
        return f'{self.naam} {self.achternaam}'

    def get_absolute_url(self):
        return reverse('Employer_detail', kwargs={'pk': self.pk})


class Student(models.Model):
    naam = models.CharField(max_length=30)
    achternaam = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f'{self.naam} {self.achternaam}'

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class Sessie(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    begeleider = models.ForeignKey(Employer, null=True, on_delete=models.SET_NULL)
    inzicht = models.IntegerField()
    kennis = models.IntegerField()
    werkhouding = models.IntegerField()
    extra = models.TextField()
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sessie {self.pk} ({self.student}, {self.begeleider})'

    def get_absolute_url(self):
        return reverse('Sessie_detail', kwargs={'pk': self.pk})
