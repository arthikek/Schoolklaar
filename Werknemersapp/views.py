
from os import path
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login

from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')





def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)

            # Set the session cookie age if the "remember_me" checkbox is checked
            if request.POST.get('remember_me'):
                request.session.set_expiry(settings.SESSION_COOKIE_AGE_REMEMBER_ME)

            # Redirect the user to the next page
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
