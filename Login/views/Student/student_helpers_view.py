
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...models import Leerling, School, Vak, LeerlingVakRating, LeerlingVakRatingHistory, Klas, Niveau
from ...serializers import LeerlingSerializer, LeerlingVakRatingSerializer




#############################################################################################################
############################################## CREATE RATING VIEW #################################################
#############################################################################################################

@api_view(['POST'])
def create_rating(request):
    if request.method != 'POST':
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    ratings = request.data.get('ratings', {})
    comments = request.data.get('comments', {})
    print('ratings', ratings)
    
    leerling = get_student_from_request(request)

    if not leerling:
        return Response({"detail": "Leerling not found"}, status=status.HTTP_400_BAD_REQUEST)

    response_data = []

    for subject_name, rating_value in ratings.items():
        subject_response = handle_subject_rating(subject_name, rating_value, comments, leerling)
        if subject_response:
            response_data.append(subject_response)

    return Response(response_data, status=status.HTTP_200_OK)


def get_student_from_request(request):
    try:
        return Leerling.objects.get(gebruiker=request.user)
    except Leerling.DoesNotExist:
        return None


def handle_subject_rating(subject_name, rating_value, comments, leerling):
    vak = Vak.objects.filter(naam=subject_name).first()
    if not vak:
        print('subject not found')
        return None

    comment = comments.get(subject_name, "")
    existing_rating,created = LeerlingVakRating.objects.get_or_create(leerling=leerling, vak=vak)

    data = {
        "leerling": leerling.pk,
        "vak": vak.pk,
        "cijfer": int(rating_value),
        "beschrijving": comment
    }

    serializer = LeerlingVakRatingSerializer(existing_rating, data=data)
    
    if serializer.is_valid():
        serializer.save()
        record_history(existing_rating, rating_value, comment)
        return {"subject": subject_name, "status": "success"}
    else:
        return {"subject": subject_name, "status": "error", "errors": serializer.errors}


def record_history(existing_rating, rating_value, comment):
    today = timezone.now().date()
    history_record, created = LeerlingVakRatingHistory.objects.get_or_create(
        leerling_vak_rating=existing_rating, date_recorded=today
    )
    if not created:
        history_record.cijfer = int(rating_value)
        history_record.beschrijving = comment
        history_record.save()
        



# Fetching available subjects
@api_view(['GET'])
def get_all_subjects(request):
    try:
        subjects = Vak.objects.all()
        if not subjects:
            return Response({"error": "No subjects found"}, status=status.HTTP_404_NOT_FOUND)
        
        subjects_data = [{"id": subject.id, "name": subject.naam} for subject in subjects] # type: ignore
        return Response(subjects_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_leerling_status(request):
    has_leerling = Leerling.objects.filter(gebruiker=request.user).exists()
    return Response({"hasLeerling": has_leerling})        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_leerling_with_secret_code(request):
    # Extract the secret code from the POST data
    secret_code = request.data.get('secret_code')
    
    # Validate the secret code and get the associated school
    try:
        school = School.objects.get(secret_code=secret_code)
    except School.DoesNotExist:
        return Response({"detail": "Invalid secret code."}, status=status.HTTP_400_BAD_REQUEST)

    # Extract other data for Leerling and use the school from the secret code
    leerling_data = {
        'naam': request.data.get('naam'),
        'achternaam': request.data.get('achternaam'),
        'email': request.data.get('email'),
        'klas': request.data.get('klas'),
        'niveau': request.data.get('niveau'),
        'school': school.pk,
        'gebruiker': request.user.id
    }

    # Validate the Leerling data using the serializer
    serializer = LeerlingSerializer(data=leerling_data)
    if serializer.is_valid(raise_exception=True):
        # Use Django ORM directly to create the Leerling instance
        leerling = Leerling.objects.create(
            naam=leerling_data['naam'],
            achternaam=leerling_data['achternaam'],
            email=leerling_data['email'],
            klas=Klas.objects.get(pk=leerling_data['klas']),
            niveau=Niveau.objects.get(pk=leerling_data['niveau']),
            school=school,
            gebruiker=request.user
        )

        # Serialize the newly created Leerling instance
        response_serializer = LeerlingSerializer(leerling)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
