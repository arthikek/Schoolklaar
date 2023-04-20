from django import forms
from .models import Leerling, Sessie 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm




class StudentForm(forms.ModelForm):
    class Meta:
        model = Leerling
        fields = ['naam', 'achternaam', 'email', 'school']

class SessieForm(forms.ModelForm):
    class Meta:
        model = Sessie
        fields = ['Leerling', 'inzicht', 'kennis', 'werkhouding', 'extra', 'datum']
        exclude = ['datum']





class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'nav'}))
