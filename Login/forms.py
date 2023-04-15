from django import forms
from .models import Leerling, Sessie , Employer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('naam', 'achternaam', 'email')
      

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Opslaan'))



class StudentForm(forms.ModelForm):
    class Meta:
        model = Leerling
        fields = ['naam', 'achternaam', 'email']

class SessieForm(forms.ModelForm):
    class Meta:
        model = Sessie
        fields = ['Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding', 'extra']
        




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'nav'}))
