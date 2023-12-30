
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, FileResponse, HttpResponseServerError, JsonResponse
from typing import Dict, Any
from .forms import StudentForm, SessieForm, MateriaalForm, SessieFormUpdate
from .models import Leerling, School, Sessie, Begeleider, Teamleider, Materiaal, Vak, Klas, Niveau
from .serializers import SessieSerializer, LeerlingSerializer, KlasSerializer, NiveauSerializer, SessieSerializer_2, LeerlingVakRatingHistory, LeerlingDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework import generics




from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LeerlingVakRating
from .serializers import LeerlingVakRatingSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *


from django.db import IntegrityError





#############################################################################################################
############################################## GET ALL SUBJECTS VIEW #################################################
#############################################################################################################


#############################################################################################################
############################################## STUDENT DETAILS #################################################
#############################################################################################################




    
# Function to retrieve and serve a specific 'Materiaal' (Material) document as a PDF attachment
def get(request, pk):
    # Fetch the document with the provided primary key or return a 404 if not found
    document = get_object_or_404(Materiaal, pk=pk)
    # Create a new HTTP response serving the document as a PDF
    response = HttpResponse(document.bestand, content_type='application/pdf')
    # Set the Content-Disposition header to trigger a file download in the browser
    response['Content-Disposition'] = f'attachment; filename="{document.bestand.name}"'
    return response





#############################################################################################################
############################################## ADD STUDENT #################################################
#############################################################################################################

# View to add a new 'Leerling' (Student) with user authentication check
class AddStudentView(LoginRequiredMixin, CreateView):
    model = Leerling
    form_class = StudentForm
    template_name = 'Login/add_student.html'

    # Redirect to the student listing page upon successful addition
    success_url = reverse_lazy('Login:student_all')
    
    # Override the form initialization to set custom form properties
    def get_form(self, form_class=None):
        form = super(AddStudentView, self).get_form(form_class)
        gebruiker = self.request.user

        # Check if the user is associated with a 'Begeleider' (guide) or 'Teamleider' (team leader)
        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        # Get the schools associated with the user based on their role
        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = School.objects.filter(id=teamleider.school.pk)
        else:
            scholen = School.objects.none()

        # Set the schools queryset for the form field based on the user's role
        form.fields['school'].queryset = scholen

        return form


        
        
        
        




#############################################################################################################
############################################## ADD Material #################################################
#############################################################################################################

class AddMateriaalView(LoginRequiredMixin, CreateView):
    model = Materiaal
    form_class = MateriaalForm
    template_name = 'Login/add_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')      
    









#############################################################################################################
############################################## Material lIST View #################################################
#############################################################################################################

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
            return Materiaal.objects.filter(leerling__isnull=True)
        else:
            return Materiaal.objects.none()







#############################################################################################################
############################################## STUDENT LIST #################################################
#############################################################################################################

# View to display a list of 'Leerling' (Student) entries with user authentication check
class StudentListView(LoginRequiredMixin, ListView):
    model = Leerling                           # The model this view operates upon
    template_name = 'Login/student_all.html'   # Template to render the list of students
    context_object_name = 'Leerling'           # Name to use for the list in the template

    # Override method to customize the default queryset retrieved from the database
    def get_queryset(self):
        # Retrieve the default queryset
        queryset = super().get_queryset()

        # Get student name from the GET request if provided (used for filtering the results)
        student_name = self.request.GET.get('student_name') 

        # Retrieve the current user
        gebruiker = self.request.user

        # Check if the current user is associated with a 'Begeleider' entry
        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()

        # Check if the current user is associated with a 'Teamleider' entry
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        # Retrieve schools based on user's association: 
        # If a 'Begeleider', get all their associated schools
        if begeleider:
            scholen = begeleider.scholen.all()
        # If a 'Teamleider', get their associated school
        elif teamleider:
            scholen = [teamleider.school]
        # If neither, return an empty queryset
        else:
            return queryset.none()

        # If there are associated schools, filter the students by those schools
        if scholen:
            queryset = queryset.filter(school__in=scholen)

        # If a student name is provided in the GET request, 
        # further filter the students by names starting with that value (case-insensitive)
        if student_name:
            queryset = queryset.filter(naam__istartswith=student_name)
            
        return queryset  # Return the customized queryset




#############################################################################################################
############################################## Details #################################################
#############################################################################################################

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Leerling
    template_name = 'Login/student_detail.html'


class StudentDetailView_2(LoginRequiredMixin, DetailView):
    model = Leerling
    template_name = 'Login/report.html'

 
    
class SessieDetailView(LoginRequiredMixin, DetailView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    
    

class MateriaalDetailView(LoginRequiredMixin, DetailView):
    model = Materiaal
    template_name = 'Login/materiaal_detail.html'
    context_object_name = 'materiaal'



#############################################################################################################
############################################## General Inforation view #################################################
#############################################################################################################

