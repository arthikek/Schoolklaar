from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Relative imports for serializers and models
from ..serializers import SessieSerializer, SessieSerializer_2
from ..models import Leerling, Sessie

#############################################################################################################
############################################## ADD Session #################################################
#############################################################################################################


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AddSessieAPIView(APIView):
    def post(self, request):
        # Create a mutable copy of the request data
        data = request.data.copy()
        
        print("Request Data:", data)
        
        # Extract the Leerling ID from the request data
        leerling_id = data.pop('Leerling')[0]  # QueryDict values are lists, so we take the first element
        # Fetch the Leerling instance using the provided ID
        leerling_instance = Leerling.objects.get(id=leerling_id)
        
        # Update the request data with the Leerling instance
        data['Leerling'] = leerling_instance.id
        
        serializer = SessieSerializer(data=data)
        print(serializer.is_valid())
        
        if serializer.is_valid():
            sessie = serializer.save(begeleider=request.user, school=leerling_instance.school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AddSessieAPIView_2(APIView):
    def post(self, request):
        # Create a mutable copy of the request data
        data = request.data.copy()

        # Extract the Leerling ID from the request data and convert it to integer
        leerling_id = data.get('Leerling')
        if leerling_id:
            leerling_id = leerling_id[0]  # Assuming it's always one ID passed

        try:
            # Attempt to convert the ID to an integer
            leerling_id = int(leerling_id)
        except (TypeError, ValueError):
            return Response({"error": "Invalid Leerling ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the Leerling instance using the provided ID
            leerling_instance = Leerling.objects.get(id=leerling_id)
        except Leerling.DoesNotExist:
            return Response({"error": "Leerling not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Initialize the serializer with the request data
        serializer = SessieSerializer_2(data=data)
        
        # Validate the data
        if serializer.is_valid():
            # Save the session instance if the data is valid
            sessie = serializer.save(begeleider=request.user, school=leerling_instance.school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Print and return the errors if validation fails
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UpdateSessieAPIView(APIView):
    def put(self, request, sessie_id):   # sessie_id is the ID of the Sessie to be updated
        try:
            sessie = Sessie.objects.get(id=sessie_id)
        except Sessie.DoesNotExist:
            return Response({"error": "Sessie not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user has the right to update this Sessie
        # You might have other logic for this
        if request.user != sessie.begeleider:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        # You may need similar logic to the POST request to handle associated data
        # For example, to handle 'Leerling' foreign key, etc.
        # Add that here if necessary

        serializer = SessieSerializer_2(instance=sessie, data=data, partial=True)  # partial=True allows for partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        
