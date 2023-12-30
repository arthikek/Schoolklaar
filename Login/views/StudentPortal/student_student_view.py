# Import statements for Django and DRF functionalities
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse

# Relative imports for models and serializers
from ...models import Leerling, Begeleider, Teamleider, School, LeerlingVakRating, LeerlingVakRatingHistory
from ...serializers import LeerlingSerializer, LeerlingDetailSerializer

# Additional imports
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

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



#test commit
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
        print("put request received")
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
                for vak in student.vakken.all(): # type: ignore
                    if vak.id not in vakken_ids:
                        student.vakken.remove(vak) # type: ignore
                
                # Add new vakken from the list
                for vak_id in vakken_ids:
                    if not student.vakken.filter(id=vak_id).exists(): # type: ignore
                        student.vakken.add(vak_id) # type: ignore
                        # Create or get the LeerlingVakRating instance
                        vak_rating, created = LeerlingVakRating.objects.get_or_create(
                            leerling=student,
                            vak_id=vak_id,
                            defaults={'cijfer': 5, 'beschrijving': 'Standaard beschrijving'}  # Default values
                        )
                      
                        # If created, also create a history record
                        LeerlingVakRatingHistory.objects.create(
                                leerling_vak_rating=vak_rating,
                                cijfer=vak_rating.cijfer,
                                beschrijving=vak_rating.beschrijving,
                                
                            )
                return Response(serializer.data)
            else:
                raise ValidationError(serializer.errors)
            
        except Leerling.DoesNotExist:
            raise NotFound("Student not found for the authenticated user.")
            
        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, pk=None):
        try:
            if pk:
                student = Leerling.objects.get(pk=pk)
            else:
                student = Leerling.objects.get(gebruiker=request.user)

            serializer = LeerlingDetailSerializer(student)
            return Response(serializer.data)

        except Leerling.DoesNotExist:
            raise NotFound("Student not found.")
        
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


