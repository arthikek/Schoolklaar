
from os import path
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')



