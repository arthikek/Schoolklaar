from math import log
from operator import is_
from typing import Any
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from pyrsistent import v
from yaml import serialize
from .forms import StudentForm, SessieForm, MateriaalForm,SessieFormUpdate
from .models import Leerling, School, Sessie, Begeleider, Teamleider,Materiaal,Vak,Klas,Niveau
from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render  
from django.http import HttpRequest, HttpResponse , FileResponse
from django.http import JsonResponse
from django.core import serializers
from .serializers import SessieSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Begeleider, Teamleider
from .serializers import SessieSerializer, LeerlingSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LeerlingSerializer  # make sure to create this serializer
from django.db.models import Q

# ...

def search_leerling(naam, achternaam):
    query = Q(naam__icontains=naam) & Q(achternaam__icontains=achternaam)
    leerling = Leerling.objects.filter(query).order_by('-naam', '-achternaam').first()
    print(leerling)
    return leerling


class StudentListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Leerling.objects.all()
        student_name = self.request.GET.get('search-input') 
        
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            return Response([], status=status.HTTP_200_OK)

        if scholen:
            queryset = queryset.filter(school__in=scholen)

        if student_name:
            queryset = queryset.filter(naam__istartswith=student_name)
        
        serializer = LeerlingSerializer(queryset, many=True)
        return Response(serializer.data)



class SessieListViewAPI(APIView):
    """
    List all sessies, or create a new sessie.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessies = Sessie.objects.all()
        gebruiker = self.request.user

        if not gebruiker.is_authenticated:
            return Response({'error': 'You need to be authenticated to access this endpoint.'})

        
        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
       
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()
        
        if begeleider:
            scholen = begeleider.scholen.all()
            
        elif teamleider:
            scholen = [teamleider.school]
           
        else:
            return Response([])

        if scholen:
            sessies = sessies.filter(Leerling__school__in=scholen)
           
            
            

    # Get the school and begeleider query parameters
        query_school_name = self.request.GET.get('school')
        query_begeleider_name = self.request.GET.get('begeleider')
        query_vak_name = self.request.GET.get('vak')
        query_niveau_name = self.request.GET.get('niveau')
        query_klas_name = self.request.GET.get('klas')
        
       
    # If the query parameters are provided, filter the sessions accordingly
        if query_school_name:
            sessies = sessies.filter(school__naam=query_school_name)
        if query_begeleider_name:
            sessies = sessies.filter(begeleider__username=query_begeleider_name)
        if query_vak_name:  
            sessies = sessies.filter(vak__naam=query_vak_name)
            print(sessies)
        if query_niveau_name:
            sessies = sessies.filter(Leerling__niveau__naam=query_niveau_name)
        if query_klas_name:
            sessies = sessies.filter(Leerling__klas__naam__icontains=query_klas_name)

        serializer = SessieSerializer(sessies.order_by('-datum'), many=True)
        return Response(serializer.data)



    

def get(request, pk):
    document = get_object_or_404(Materiaal, pk=pk)
    response = HttpResponse(document.bestand, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{document.bestand.name}"'
    return response



class DeleteSessieView(LoginRequiredMixin, DeleteView):
    model = Sessie
    template_name = 'Login/delete_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')






class DeleteMateriaalView(LoginRequiredMixin, DeleteView):
    model = Materiaal
    template_name = 'Login/delete_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')

class UpdateMateriaalView(LoginRequiredMixin, UpdateView):
    model = Materiaal
    form_class = MateriaalForm
    template_name = 'Login/update_materiaal.html'
    success_url = reverse_lazy('Login:materiaal_all')

 

class UpdateSessieView(LoginRequiredMixin, UpdateView):
    model = Sessie
    form_class = SessieFormUpdate
    template_name = 'Login/update_sessie.html'
    success_url = reverse_lazy('Login:sessie_all')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class AddStudentView(LoginRequiredMixin, CreateView):
    model = Leerling
    form_class = StudentForm
    template_name = 'Login/add_student.html'
    success_url = reverse_lazy('Login:student_all')
    
    def get_form(self, form_class=None):
        form = super(AddStudentView, self).get_form(form_class)
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = School.objects.filter(id=teamleider.school.pk)
        else:
            scholen = School.objects.none()

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
            school = School.objects.get(id=leerling.school.id)
            
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
            print(sessie)
            sessie.save()

        
            return redirect('Login:sessie_all')  # assuming you want to redirect to the list of all sessions

        else:
            return render(request, 'Login/add_sessie.html', {})
    except:
        return render(request, 'Login/add_sessie.html', {})






class SessieListView(LoginRequiredMixin, ListView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    context_object_name = 'sessies'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        models = ['School', 'Begeleider', 'Vak', 'Leerling', 'Niveau','Klas']
        for model in models:
            context[model.lower() + 's'] = globals()[model].objects.all()
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

    

class StudentListView(LoginRequiredMixin, ListView):
    model = Leerling
    template_name = 'Login/student_all.html'
    context_object_name = 'Leerling'
    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.GET.get('student_name') 
        gebruiker = self.request.user

        begeleider = Begeleider.objects.filter(gebruiker=gebruiker).first()
        teamleider = Teamleider.objects.filter(gebruiker=gebruiker).first()

        if begeleider:
            scholen = begeleider.scholen.all()
        elif teamleider:
            scholen = [teamleider.school]
        else:
            return queryset.none()

        if scholen:
            queryset = queryset.filter(school__in=scholen)

        if student_name:
            queryset = queryset.filter(naam__istartswith=student_name)  # filter the queryset by the student_name value
            
        return queryset

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Leerling
    template_name = 'Login/student_detail.html'
    
    
class SessieDetailView(LoginRequiredMixin, DetailView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    
    

class MateriaalDetailView(LoginRequiredMixin, DetailView):
    model = Materiaal
    template_name = 'Login/materiaal_detail.html'
    context_object_name = 'materiaal'

