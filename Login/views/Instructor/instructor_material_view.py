from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import NotFound, ValidationError

from ...models import Begeleider, Materiaal, Vak
from ...serializers import MateriaalSerializer

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
                materiaal_list = materiaal_list.filter(vak_id=vak.id) # type: ignore
            
            # Serialize the data
            serializer = MateriaalSerializer(materiaal_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except DatabaseError:
            # This will catch any database related errors
            return Response({"error": "Database error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # This is a general exception handler. Be cautious when using it.
            return Response({"error": f"An error occurred: {str(e)}."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
                    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CreateMateriaalAPIView(generics.CreateAPIView):
    queryset = Materiaal.objects.all()
    serializer_class = MateriaalSerializer
