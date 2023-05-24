from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import StudentForm, SessieForm, MateriaalForm,SessieFormUpdate
from .models import Leerling, School, Sessie, Begeleider, Teamleider,Materiaal
from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render  
from django.http import HttpResponse , FileResponse



def get(request, pk):
    document = get_object_or_404(Materiaal, pk=pk)
    response = HttpResponse(document.bestand, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.bestand.name}"'
    return response



class DeleteSessieView(LoginRequiredMixin, DeleteView):
    model = Sessie
    template_name = 'Login/delete_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')






class DeleteMateriaalView(LoginRequiredMixin, DeleteView):
    model = Materiaal
    template_name = 'Login/delete_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')

class UpdateMateriaalView(LoginRequiredMixin, UpdateView):
    model = Materiaal
    form_class = MateriaalForm
    template_name = 'Login/update_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')

 

class UpdateSessieView(LoginRequiredMixin, UpdateView):
    model = Sessie
    form_class = SessieFormUpdate
    template_name = 'Login/update_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class AddStudentView(LoginRequiredMixin, CreateView):
    model = Leerling
    form_class = StudentForm
    template_name = 'Login/add_student.html'
    success_url = reverse_lazy('Login:student_all')
    
    def get_form(self, form_class=None):
        form = super(AddStudentView, self).get_form(form_class)
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = School.objects.filter(id=teamleider.school.pk)
        else:
            scholen = School.objects.none()

        form.fields['school'].queryset = scholen

        return form


class AddMateriaalView(LoginRequiredMixin, CreateView):
    model = Materiaal
    form_class = MateriaalForm
    template_name = 'Login/add_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')                            


class AddSessieView(LoginRequiredMixin, CreateView):
    model = Sessie
    form_class = SessieForm
    template_name = 'Login/add_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')
    
    def get_form(self, form_class=None):
        form = super(AddSessieView, self).get_form(form_class)
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            scholen = []

        form.fields['Leerling'].queryset = Leerling.objects.filter(school__in=scholen)

        return form

    def form_valid(self, form):
        form.instance.begeleider = self.request.user
        return super().form_valid(form)


class SessieListView(LoginRequiredMixin, ListView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    context_object_name = 'sessies'
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.GET.get('student_name')  
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            return queryset.none()

        if scholen:
            queryset = queryset.order_by('-datum').filter(Leerling__school__in=scholen)

        if student_name:
            queryset = queryset.order_by('-datum').filter(Leerling__naam__istartswith=student_name)

        return queryset


class MateriaalListView(LoginRequiredMixin, ListView):
    model = Materiaal
    template_name = 'Login/materiaal_all.html'
    context_object_name = 'materiaal'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.GET.get('student_name')  
        gebruiker = self.request.user
            

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        if begeleider:
            return Materiaal.objects.all()
        else:
            return Materiaal.objects.none()

    

class StudentListView(LoginRequiredMixin, ListView):
    model = Leerling
    template_name = 'Login/student_all.html'
    context_object_name = 'Leerling'
    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.GET.get('student_name') 
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            return queryset.none()

        if scholen:
            queryset = queryset.filter(school__in=scholen)

        if student_name:
            queryset = queryset.filter(naam__istartswith=student_name)  # filter the queryset by the student_name value
            
        return queryset

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Leerling
    template_name = 'Login/student_detail.html'
    
    
class SessieDetailView(LoginRequiredMixin, DetailView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    
    

class MateriaalDetailView(LoginRequiredMixin, DetailView):
    model = Materiaal
    template_name = 'Login/materiaal_detail.html'
    context_object_name = 'materiaal'

