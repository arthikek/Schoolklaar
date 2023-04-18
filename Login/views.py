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
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin

class DeleteSessieView(LoginRequiredMixin, DeleteView):
    model = Sessie
    template_name = 'Login/delete_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')


class UpdateSessieView(LoginRequiredMixin, UpdateView):
    model = Sessie
    form_class = SessieForm
    template_name = 'Login/update_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')


class AddStudentView(LoginRequiredMixin, CreateView):
    model = Leerling
    form_class = StudentForm
    template_name = 'Login/add_student.html'
    success_url = reverse_lazy('Login:student_all')


class AddSessieView(LoginRequiredMixin, CreateView):
    model = Sessie
    form_class = SessieForm
    template_name = 'Login/add_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Leerling
    template_name = 'Login/student_detail.html'


class SessieListView(LoginRequiredMixin, ListView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    context_object_name = 'sessies'

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.GET.get('student_name') # get the student_name value from the input field
        if student_name:
            queryset = queryset.filter(Leerling__naam=student_name) # filter the queryset by the student_name value
        return queryset


class SessieDetailView(LoginRequiredMixin, DetailView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'


class StudentListView(LoginRequiredMixin, ListView):
    model = Leerling
    template_name = 'Login/student_all.html'
    context_object_name = 'Leerling'
