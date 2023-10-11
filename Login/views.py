from math import log
from operator import is_
from typing import Any
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, FileResponse, HttpResponseServerError, JsonResponse
from django.db.models import Q, QuerySet
from django.core import serializers
from django.core.files.images import ImageFile
from .forms import StudentForm, SessieForm, MateriaalForm, SessieFormUpdate
from .models import Leerling, School, Sessie, Begeleider, Teamleider, Materiaal, Vak, Klas, Niveau
from .serializers import SessieSerializer, LeerlingSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pyrsistent import v
from yaml import serialize

from django.contrib.auth import authenticate
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LeerlingVakRating
from .serializers import LeerlingVakRatingSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication






from django.db import IntegrityError


@api_view(['POST'])
def create_rating(request):
    # If the incoming request is POST
    if request.method == 'POST':
        # Extract ratings and comments from the request data
        ratings = request.data.get('ratings', {})
        comments = request.data.get('comments', {})

        # Attempt to retrieve the Leerling (student) based on the user making the request
        try:
            leerling = Leerling.objects.get(gebruiker=request.user)
        except Leerling.DoesNotExist:
            # Return an error response if the student is not found
            return Response({"detail": "Leerling not found"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = []

        # Loop through each rating in the ratings dictionary
        for subject_name, rating_value in ratings.items():
            try:
                # Attempt to get the corresponding Vak (subject) for the provided subject name
                vak = Vak.objects.get(naam=subject_name)
            except Vak.DoesNotExist:
                # If the subject isn't found, skip processing this rating and move to the next
                continue

            # Fetch the associated comment for this subject if it exists
            comment = comments.get(subject_name, "")

            # Check if a rating already exists for this combination of student and subject
            existing_rating = LeerlingVakRating.objects.filter(leerling=leerling, vak=vak).first()
            
            # Prepare the data to be used with the serializer
            data = {
                "leerling": leerling.pk,
                "vak": vak.pk,
                "cijfer": rating_value,
                "beschrijving": comment
            }

            # If an existing rating was found, initialize the serializer to update the rating
            if existing_rating:
                serializer = LeerlingVakRatingSerializer(existing_rating, data=data)
            else:
                # If no existing rating was found, initialize the serializer to create a new rating
                serializer = LeerlingVakRatingSerializer(data=data)
            
            # Check if the serializer data is valid
            if serializer.is_valid():
                # Save the rating (either creates a new one or updates the existing)
                serializer.save()
                # Append the




    

# Function to search a 'Leerling' (student) based on given first and last names
def search_leerling(naam, achternaam):
    # Construct a query to find a student whose name contains 'naam' and surname contains 'achternaam'
    query = Q(naam__icontains=naam) & Q(achternaam__icontains=achternaam)
    # Retrieve the first student that matches the criteria, ordered by name and surname in descending order
    leerling = Leerling.objects.filter(query).order_by('-naam', '-achternaam').first()
    
    return leerling

# View to get details of a student authenticated by JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentDetailAPI(APIView):

    def post(self, request):            
        # Retrieve the student associated with the authenticated user
        student = get_object_or_404(Leerling, gebruiker=request.user)
        
        # Serialize the student data to return
        serializer = LeerlingSerializer(student)
        return Response(serializer.data)

# View to list students based on authentication and potential search criteria
class StudentListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Initially set the queryset to all students
        queryset = Leerling.objects.all()
        # Get the search input from the request, if provided
        student_name = self.request.GET.get('search-input') 
        
        # Determine the user making the request
        gebruiker = self.request.user

        # Check if the user is associated with a 'Begeleider' (guide) or 'Teamleider' (team leader)
        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        # Get the schools associated with the user based on their role
        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            # If user is neither, return an empty response
            return Response([], status=status.HTTP_200_OK)

        # Filter students based on the associated schools
        if scholen:
            queryset = queryset.filter(school__in=scholen)

        # Further filter students if a search name is provided
        if student_name:
            queryset = queryset.filter(naam__istartswith=student_name)
        
        # Serialize the filtered list of students
        serializer = LeerlingSerializer(queryset, many=True)
        return Response(serializer.data)


class SessieListViewAPI(APIView):
    """
    List all sessies (sessions), or create a new sessie (session).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Initially set the queryset to all sessions
        sessies = Sessie.objects.all()
        # Determine the user making the request
        gebruiker = self.request.user

        # Check if the user is authenticated
        if not gebruiker.is_authenticated:
            return Response({'error': 'You need to be authenticated to access this endpoint.'})

        # Check if the user is associated with a 'Begeleider' (guide) or 'Teamleider' (team leader)
        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        # Get the schools associated with the user based on their role
        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            # If user is neither, return an empty response
            return Response([])

        # Filter sessions based on the schools associated with the students participating in them
        if scholen:
            sessies = sessies.filter(Leerling__school__in=scholen)

            
            

    # Get the school and begeleider query parameters
        query_school_name = self.request.GET.get('school')
        query_begeleider_name = self.request.GET.get('begeleider')
        query_vak_name = self.request.GET.get('vak')
        query_niveau_name = self.request.GET.get('niveau')
        query_klas_name = self.request.GET.get('klas')
        query_leerling_pk = self.request.GET.get('leerling')
        
        
       
    # If the query parameters are provided, filter the sessions accordingly
        if query_school_name:
            sessies = sessies.filter(school__naam=query_school_name)
        if query_begeleider_name:
            sessies = sessies.filter(begeleider__username=query_begeleider_name)
        if query_vak_name:  
            sessies = sessies.filter(vak__naam=query_vak_name)
            
        if query_niveau_name:
            sessies = sessies.filter(Leerling__niveau__naam=query_niveau_name)
        if query_klas_name:
            sessies = sessies.filter(Leerling__klas__naam__icontains=query_klas_name)
        if query_leerling_pk:
            sessies= sessies.filter(Leerling__pk=query_leerling_pk)

        serializer = SessieSerializer(sessies.order_by('-datum'), many=True)
        return Response(serializer.data)



    
# Function to retrieve and serve a specific 'Materiaal' (Material) document as a PDF attachment
def get(request, pk):
    # Fetch the document with the provided primary key or return a 404 if not found
    document = get_object_or_404(Materiaal, pk=pk)
    # Create a new HTTP response serving the document as a PDF
    response = HttpResponse(document.bestand, content_type='application/pdf')
    # Set the Content-Disposition header to trigger a file download in the browser
    response['Content-Disposition'] = f'attachment; filename="{document.bestand.name}"'
    return response

# View to delete a specific 'Sessie' (Session) with user authentication check
class DeleteSessieView(LoginRequiredMixin, DeleteView):
    model = Sessie
    template_name = 'Login/delete_sessie.html'
    # Redirect to the session listing page upon successful deletion
    success_url = reverse_lazy('Login:sessie_all')

# View to delete a specific 'Materiaal' (Material) with user authentication check
class DeleteMateriaalView(LoginRequiredMixin, DeleteView):
    model = Materiaal
    template_name = 'Login/delete_materiaal.html'
    # Redirect to the material listing page upon successful deletion
    success_url = reverse_lazy('Login:materiaal_all')

# View to update details of a specific 'Materiaal' (Material) with user authentication check
class UpdateMateriaalView(LoginRequiredMixin, UpdateView):
    model = Materiaal
    form_class = MateriaalForm
    template_name = 'Login/update_materiaal.html'
    # Redirect to the material listing page upon successful update
    success_url = reverse_lazy('Login:materiaal_all')

# View to update details of a specific 'Sessie' (Session) with user authentication check
class UpdateSessieView(LoginRequiredMixin, UpdateView):
    model = Sessie
    form_class = SessieFormUpdate
    template_name = 'Login/update_sessie.html'
    # Redirect to the session listing page upon successful update
    success_url = reverse_lazy('Login:sessie_all')
    
    # Handle the validation and saving of the form
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

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

    def form_valid(self, form):
        form.instance.begeleider = self.request.user
        leerling_id = form.cleaned_data.get('Leerling')
        leerling = get_object_or_404(Leerling, id=leerling_id)

        # Assign the school automatically based on the chosen student
        form.instance.school = leerling.school

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        models = ['School', 'Begeleider', 'Vak', 'Leerling', 'Niveau','Klas']
        for model in models:
            context[model.lower() + 's'] = globals()[model].objects.all()
        return context



@login_required
def add_sessie_view(request):
    try:
        if request.method == 'POST':
            # Access form data using request.POST
            leerling_voornaam = request.POST.get('Leerling').split()[0]
            leerling_achternaam = request.POST.get('Leerling').split()[1]
            inzicht = request.POST.get('inzicht')
            kennis = request.POST.get('kennis')
            werkhouding = request.POST.get('werkhouding')
            extra = request.POST.get('extra')
            school_id = request.POST.get('school')
            vak_naam = request.POST.get('vak')
        
            # Fetch related objects
            leerling = search_leerling(leerling_voornaam, leerling_achternaam)
            school = School.objects.get(id=leerling.school.id) # type:ignore
            
            vak = Vak.objects.get(naam=vak_naam)
            begeleider = request.user  # assuming the user is logged in

            # Create and save new Sessie
            sessie = Sessie(
                Leerling=leerling, 
                begeleider=begeleider, 
                inzicht=inzicht, 
                kennis=kennis, 
                werkhouding=werkhouding, 
                extra=extra, 
                school=school, 
                vak=vak
            )
            
            sessie.save()

            
            return redirect('Login:sessie_all')  # assuming you want to redirect to the list of all sessions

        else:
            return render(request, 'Login/add_sessie.html', {})

    except:
        return render(request, 'Login/add_sessie.html', {})
        




# View to display a list of 'Sessie' (Session) entries with user authentication check
class SessieListView(LoginRequiredMixin, ListView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'      # Template to render the list of sessions
    context_object_name = 'sessies'                  # Name to use for the list in the template

    # Override method to add additional context data for the template
    def get_context_data(self, **kwargs):
        # Retrieve context data from parent class
        context = super().get_context_data(**kwargs)

        # Get the currently authenticated user
        user = self.request.user
        # Initialize with no schools, this will be filled based on user's role
        user_schools = School.objects.none()  
      
        # Check if the current user is a 'Begeleider' and retrieve their associated schools
        if hasattr(user, 'begeleider'):
            user_schools = user.begeleider.scholen.all() #type:ignore
            
        # Check if the current user is a 'Teamleider' and retrieve their associated school
        if hasattr(user, 'teamleider'):
            user_schools = School.objects.filter(id=user.teamleider.school.id) #type:ignore

        # If user is neither 'Begeleider' nor 'Teamleider', the original context is returned without additions
        if not user_schools:
            return context

        # Populate context with lists of various models for use in the template
        models = ['Vak', 'Leerling', 'Niveau', 'Klas']
        for model in models:
            context[model.lower() + 's'] = globals()[model].objects.all()

        # Additional models, specifically for Begeleiders and Schools, 
        # which require some filtering based on the user's associations
        models2 = ['Begeleider', 'School']
        for model in models2:
            if model == 'Begeleider':
                # Get 'Begeleiders' associated with the schools related to the current user
                context[model.lower() + 's'] = globals()[model].objects.filter(scholen__in=user_schools).distinct()
            elif model == 'School':
                # For Schools, we can directly use the schools associated with the user
                context[model.lower() + 's'] = user_schools

        return context





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

