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
from .serializers import SessieSerializer, LeerlingSerializer, KlasSerializer, NiveauSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pyrsistent import v
from yaml import serialize
from rest_framework import generics
from django.contrib.auth import authenticate
from django.http import JsonResponse

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
############################################## CREATE RATING VIEW #################################################
#############################################################################################################

@api_view(['POST'])
def create_rating(request):
    print('data', request.data)
    if request.method == 'POST':
        ratings = request.data.get('ratings', {})
        comments = request.data.get('comments', {})

        try:
            leerling = Leerling.objects.get(gebruiker=request.user)
        except Leerling.DoesNotExist:
            return Response({"detail": "Leerling not found"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = []

        for subject_name, rating_value in ratings.items():
            try:
                vak = Vak.objects.get(naam=subject_name)
            except Vak.DoesNotExist:
                print('subject not found')
                continue

            comment = comments.get(subject_name, "")
            existing_rating = LeerlingVakRating.objects.filter(leerling=leerling, vak=vak).first()
            
            data = {
                "leerling": leerling.pk,
                "vak": vak.pk,
                "cijfer": int(rating_value),  # Convert to integer
                "beschrijving": comment
            }

            if existing_rating:
                serializer = LeerlingVakRatingSerializer(existing_rating, data=data)
            else:
                serializer = LeerlingVakRatingSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                response_data.append({"subject": subject_name, "status": "success"})
            else:
                response_data.append({"subject": subject_name, "status": "error", "errors": serializer.errors})

        return Response(response_data, status=status.HTTP_200_OK)
        

#############################################################################################################
############################################## GET ALL SUBJECTS VIEW #################################################
#############################################################################################################

# Fetching available subjects
@api_view(['GET'])
def get_all_subjects(request):
    try:
        subjects = Vak.objects.all()
        if not subjects:
            return Response({"error": "No subjects found"}, status=status.HTTP_404_NOT_FOUND)
        
        subjects_data = [{"id": subject.id, "name": subject.naam} for subject in subjects]
        return Response(subjects_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Function to search a 'Leerling' (student) based on given first and last names
def search_leerling(naam, achternaam):
    # Construct a query to find a student whose name contains 'naam' and surname contains 'achternaam'
    query = Q(naam__icontains=naam) & Q(achternaam__icontains=achternaam)
    # Retrieve the first student that matches the criteria, ordered by name and surname in descending order
    leerling = Leerling.objects.filter(query).order_by('-naam', '-achternaam').first()
    
    return leerling



#############################################################################################################
############################################## STUDENT DETAILS #################################################
#############################################################################################################

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentDetailAPI(APIView):

    def post(self, request):            
        try:
            # Retrieve the student associated with the authenticated user
            student = Leerling.objects.get(gebruiker=request.user)
            
            # Serialize the student data to return
            serializer = LeerlingSerializer(student)
            return Response(serializer.data)
        
        except Leerling.DoesNotExist:
            raise NotFound("Student not found for the authenticated user.")
        
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            # Retrieve the student associated with the authenticated user
            student = Leerling.objects.get(gebruiker=request.user)

            # Deserialize the request data to update the student
            serializer = LeerlingSerializer(student, data=request.data, partial=True)
            
            if serializer.is_valid():
                student = serializer.save()
                
                # Handle the vakken field manually
                vakken_ids = request.data.get('vakken', [])
                
                # Remove existing vakken not in the new list
                for vak in student.vakken.all():
                    if vak.id not in vakken_ids:
                        student.vakken.remove(vak)
                
                # Add new vakken from the list
                for vak_id in vakken_ids:
                    if not student.vakken.filter(id=vak_id).exists():
                        student.vakken.add(vak_id)
                
                return Response(serializer.data)
            else:
                raise ValidationError(serializer.errors)
            
        except Leerling.DoesNotExist:
            raise NotFound("Student not found for the authenticated user.")
            
        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#############################################################################################################
############################################## STUDENT LIST #################################################
#############################################################################################################

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



#############################################################################################################
############################################## SESSION API #################################################
#############################################################################################################

class SessieListViewAPI(APIView):
    """
    List all sessies (sessions), or create a new sessie (session).
    """


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



#############################################################################################################
############################################## DELETE VIEW #################################################
#############################################################################################################

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

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AddStudentAPIView(APIView):
    def post(self, request):
        print('request', request.data)
        try:
            gebruiker = request.data['gebruiker']
            user = User.objects.get(username=gebruiker)
            begeleider = Begeleider.objects.filter(gebruiker=user).first()
            teamleider = Teamleider.objects.filter(gebruiker=user).first()
            
            # Get the schools associated with the user based on their role
            if begeleider:
                scholen = begeleider.scholen.all()
            elif teamleider:
                scholen = School.objects.filter(id=teamleider.school.pk)
            else:
                scholen = School.objects.none()

            # Restrict the schools in the incoming data
            if 'school' in request.data and int(request.data['school']) not in [school.id for school in scholen]:
                return Response({"error": "Invalid school for this user."}, status=status.HTTP_400_BAD_REQUEST)

            data = request.data.copy()  # Create a mutable copy of the data
            if 'school' in data:
                data['school'] = int(data['school'])  # Convert to integer
            serializer = LeerlingSerializer(data=data)

            print('check 3')
            print('serializer', serializer)
            serializer.is_valid(raise_exception=True)  # Raises a serializers.ValidationError if not valid
            print('check 4')
            serializer.save()  # Create the new Leerling
            print('check 5')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            print(e)
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the error for debugging purposes
            print(e)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#############################################################################################################
############################################## ADD Material #################################################
#############################################################################################################

class AddMateriaalView(LoginRequiredMixin, CreateView):
    model = Materiaal
    form_class = MateriaalForm
    template_name = 'Login/add_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')      
    

                    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CreateMateriaalAPIView(generics.CreateAPIView):
    queryset = Materiaal.objects.all()
    serializer_class = MateriaalSerializer





#############################################################################################################
############################################## ADD Session #################################################
#############################################################################################################

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


class AddSessieAPIView(LoginRequiredMixin, APIView):
    def post(self, request):
        serializer = SessieSerializer(data=request.data)
        if serializer.is_valid():
            sessie = serializer.save()

            sessie.begeleider = request.user
            leerling_id = serializer.validated_data.get('Leerling')
            leerling = get_object_or_404(Leerling, id=leerling_id)
            sessie.school = leerling.school
            sessie.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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



########### GET ALL SUBJECTS ###############
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class MateriaalListApiView(APIView):    
    def get(self, request):
        try:
            gebruiker = request.user
   
            begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
            if begeleider:
                materiaal_list = Materiaal.objects.filter(leerling__isnull=True)
            else:
                materiaal_list = Materiaal.objects.none()

            # Serialize the data
            serializer = MateriaalSerializer(materiaal_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except DatabaseError:
            # This will catch any database related errors
            return Response({"error": "Database error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # This is a general exception handler. Be cautious when using it.
            return Response({"error": f"An error occurred: {str(e)}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


####### GET INIDIVIDUAL SUBJECT ##########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class IndividualMateriaalListApiView(APIView):    
    def get(self, request):
        try:
            gebruiker = request.user
   
            begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
            if begeleider:
                materiaal_list = Materiaal.objects.filter(leerling__isnull=True)
            else:
                materiaal_list = Materiaal.objects.none()

            # Retrieve the vak_slug from the request's query parameters
            vak_slug = request.query_params.get('vak_slug', None)
            
            if vak_slug:
                # Fetch the Vak object based on its slug
                vak = Vak.objects.filter(naam=vak_slug).first()
                if not vak:
                    raise NotFound(f"Vak with slug '{vak_slug}' not found.")
                
                # Use the retrieved Vak's ID to filter the Materiaal entries
                materiaal_list = materiaal_list.filter(vak_id=vak.id)
            
            # Serialize the data
            serializer = MateriaalSerializer(materiaal_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except DatabaseError:
            # This will catch any database related errors
            return Response({"error": "Database error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # This is a general exception handler. Be cautious when using it.
            return Response({"error": f"An error occurred: {str(e)}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class GeneralContextAPIView(APIView):
    def get(self, request):
        try:
            print("Received a request")
            context = {
                'schools': SchoolSerializer(School.objects.all(), many=True).data,
                'begeleiders': BegeleiderSerializer(Begeleider.objects.all(), many=True).data,
                'teamleiders': TeamleiderSerializer(Teamleider.objects.all(), many=True).data,
                'vakken': VakSerializer(Vak.objects.all(), many=True).data,
                'leerlings': LeerlingSerializer(Leerling.objects.all(), many=True).data,
                'klassen': KlasSerializer(Klas.objects.all(), many=True).data,
                'niveaus': NiveauSerializer(Niveau.objects.all(), many=True).data,
            }
            return Response(context)

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error occurred: {e}")
            
            # Return a JSON response indicating the error
            error_data = {
                "error": "An unexpected error occurred on the server.",
                "detail": str(e)
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)