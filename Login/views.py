from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import StudentForm, SessieForm
from .models import Leerling, Sessie, Employer
from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class DeleteSessieView(DeleteView):
    model = Sessie
    template_name = 'Login/delete_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')



class UpdateSessieView(UpdateView):
    model = Sessie
    form_class = SessieForm
    template_name = 'Login/update_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')



class AddStudentView(CreateView):
    model = Leerling
    form_class = StudentForm
    template_name = 'Login/add_student.html'
    success_url = reverse_lazy('Login:student_all')


class AddSessieView(CreateView):
    model = Sessie
    form_class = SessieForm
    template_name = 'Login/add_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')


class StudentDetailView(DetailView):
    model = Leerling
    template_name = 'Login/student_detail.html'


class SessieListView(ListView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    context_object_name = 'sessies'
   
  


class SessieDetailView(DetailView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'


class StudentListView(ListView):
    model = Leerling
    template_name = 'Login/student_all.html'
    context_object_name = 'Student'
   


