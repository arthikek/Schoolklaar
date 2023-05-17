from django import forms
from .models import Leerling, Sessie, Materiaal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm




class StudentForm(forms.ModelForm):
    class Meta:
        model = Leerling
        fields = ['naam', 'achternaam', 'email', 'school','niveau','klas']

class SessieForm(forms.ModelForm):
    class Meta:
        model = Sessie
        fields = ['Leerling', 'inzicht', 'kennis', 'werkhouding', 'vak','extra', 'datum']
        exclude = ['datum']




class MateriaalForm(forms.ModelForm):
    class Meta:
        model = Materiaal
        fields = '__all__'



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'nav'}))
