from django.db import DatabaseError
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from ...models import Leerling, Sessie, Begeleider, Teamleider, School, Niveau, Vak, Klas, Materiaal
from rest_framework.decorators import api_view
from ...serializers import (
    SessieSerializer, SessieSerializer_2, MateriaalSerializer, 
    SchoolSerializer, BegeleiderSerializer, TeamleiderSerializer, 
    LeerlingSerializer, VakSerializer, KlasSerializer, NiveauSerializer
)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class GeneralContextAPIView(APIView):
    def get(self, request):
        try:
            user = request.user

            # Initialize queryset variables
            schools_qs = School.objects.none()
            begeleiders_qs = Begeleider.objects.none()
            teamleiders_qs = Teamleider.objects.none()
            sessies_qs = Sessie.objects.none()

            if Begeleider.objects.filter(gebruiker=user).exists():
                begeleider = Begeleider.objects.get(gebruiker=user)
                schools_qs = begeleider.scholen.all()
                begeleiders_qs = Begeleider.objects.filter(scholen__in=schools_qs)
                sessies_qs = Sessie.objects.filter(school__in=schools_qs).order_by('-datum')
            elif Teamleider.objects.filter(gebruiker=user).exists():
                teamleider = Teamleider.objects.get(gebruiker=user)
                schools_qs = School.objects.filter(id=teamleider.school.id) # type: ignore
                teamleiders_qs = Teamleider.objects.filter(school=teamleider.school)
                sessies_qs = Sessie.objects.filter(school=teamleider.school).order_by('-datum')

            context = {
                'schools': SchoolSerializer(schools_qs, many=True).data,
                'begeleiders': BegeleiderSerializer(begeleiders_qs, many=True).data,
                'teamleiders': TeamleiderSerializer(teamleiders_qs, many=True).data,
                'vakken': VakSerializer(Vak.objects.all(), many=True).data,
                'leerlings': LeerlingSerializer(Leerling.objects.filter(school__in=schools_qs), many=True).data,
                'klassen': KlasSerializer(Klas.objects.all(), many=True).data,
                'niveaus': NiveauSerializer(Niveau.objects.all(), many=True).data,
                'sessies': SessieSerializer(sessies_qs, many=True).data
            }

            return Response(context)

        except Exception as e:
            print(f"Error occurred: {e}")
            error_data = {
                "error": "An unexpected error occurred on the server.",
                "detail": str(e)
            }
            return Response(error_data, status=HTTP_500_INTERNAL_SERVER_ERROR)





