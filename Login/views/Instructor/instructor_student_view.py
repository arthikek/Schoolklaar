
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

from ...models import Leerling, Begeleider, Teamleider, School
from ...serializers import LeerlingSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes



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
            if 'school' in request.data and int(request.data['school']) not in [school.id for school in scholen]: # type: ignore
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
        
        