from django import forms
from .models import Leerling, Sessie, Materiaal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput



class StudentForm(forms.ModelForm):
    class Meta:
        model = Leerling
        fields = '__all__'

class SessieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SessieForm, self).__init__(*args, **kwargs)
        self.fields['Leerling'].widget = forms.Select()
        
    class Meta:
        model = Sessie
        fields = '__all__'
        exclude=['school','begeleider']

class SessieFormUpdate(forms.ModelForm):
    class Meta: 
        model = Sessie
        fields = '__all__'


class MateriaalForm(forms.ModelForm):
    class Meta:
        model = Materiaal
        fields = '__all__'



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'nav'}))
