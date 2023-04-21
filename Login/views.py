from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import StudentForm, SessieForm
from .models import Leerling, School, Sessie, Begeleider, Teamleider
from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse

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
    
    def get_form(self, form_class=None):
        form = super(AddStudentView, self).get_form(form_class)
        user = self.request.user

        begeleider = Begeleider.objects.filter(user=user).first()
        teamleider = Teamleider.objects.filter(user=user).first()

        if begeleider:
            schools = begeleider.school.all()
        elif teamleider:
            schools = [teamleider.school]
        else:
            schools = []
            
        schools_names = [school.naam for school in schools]

        form.fields['school'].queryset = School.objects.filter(naam__in=schools_names)

        return form    

class AddSessieView(LoginRequiredMixin, CreateView):
    model = Sessie
    form_class = SessieForm
    template_name = 'Login/add_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')

    def form_valid(self, form):
        sessie = form.save(commit=False)
        sessie.begeleider = self.request.user
        sessie.save()
        self.object = sessie  # Set self.object to the saved instance
        return redirect(self.get_success_url())

    def get_form(self, form_class=None):
        form = super(AddSessieView, self).get_form(form_class)
        user = self.request.user

        begeleider = Begeleider.objects.filter(user=user).first()
        teamleider = Teamleider.objects.filter(user=user).first()

        if begeleider:
            schools = begeleider.school.all()
        elif teamleider:
            schools = [teamleider.school]
        else:
            schools = []

        form.fields['Leerling'].queryset = Leerling.objects.filter(school__in=schools)
        return form

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
        user = self.request.user

        # Check if the user is a Begeleider or Teamleider
        begeleider = Begeleider.objects.filter(user=user).first()
        teamleider = Teamleider.objects.filter(user=user).first()

        # Get the school connected to the user
        if begeleider:
            schools = begeleider.school.all()
        elif teamleider:
            schools = [teamleider.school]
        else:
            # Return an empty queryset if the user is not a Begeleider or Teamleider
            return queryset.none()

        if schools:
            queryset = queryset.filter(Leerling__school__in=schools)

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

    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Check if the user is a Begeleider or Teamleider
        begeleider = Begeleider.objects.filter(user=user).first()
        teamleider = Teamleider.objects.filter(user=user).first()

        # Get the school connected to the user
        if begeleider:
            schools = begeleider.school.all()
        elif teamleider:
            schools = [teamleider.school]
        else:
            # Return an empty queryset if the user is not a Begeleider or Teamleider
            return queryset.none()
        
        print(schools)
        if schools:
            queryset = queryset.filter(school__in=schools)
            print(queryset)

        return queryset