from rest_framework.views import APIView
from rest_framework.response import Response
from ...models import Sessie, Begeleider, Teamleider
from ...serializers import SessieSerializer
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



