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

import io, logging
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, LongTable, Image 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.template.loader import render_to_string

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image as PilImage
from io import BytesIO

logger = logging.getLogger(__name__)
matplotlib.use('Agg')  # Ensure matplotlib is in non-interactive mode






def generate_sessie_summary(request, student_pk):
    try:
        # Get the Leerling object based on the provided student_pk
        student = get_object_or_404(Leerling, pk=student_pk)

        # Get all the related Sessie instances for the student
        sessions = Sessie.objects.filter(Leerling=student).order_by('-datum')

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object using the buffer as its "file".
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        # Build the content for the PDF
        content = []

            # Create the table data for the sessions
        table_data = [['sessie datum', 'inzicht', 'kennis', 'werkhouding']]
        inzicht_data = []
        kennis_data = []
        werkhouding_data = []
        for session in sessions:
            session_data = [
                session.datum,
                session.inzicht,
                session.kennis,
                session.werkhouding
            ]
            table_data.append(session_data)
            inzicht_data.append(session.inzicht)
            kennis_data.append(session.kennis)
            werkhouding_data.append(session.werkhouding)
            # Convert session.extra to a Paragraph with appropriate styles
            extra_paragraph = Paragraph(session.extra, style=getSampleStyleSheet()["BodyText"])
            extra_data = [extra_paragraph]
            table_data.append(extra_data) # type: ignore
        inzicht_data=inzicht_data[::-1]
        kennis_data=kennis_data[::-1]
        werkhouding_data=werkhouding_data[::-1]
        # Define the table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#56b6ed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 1), (-1, -1), 5),
            ('RIGHTPADDING', (0, 1), (-1, -1), 5),
        ])

        # Create the table
        table = Table(table_data, repeatRows=1, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch])

        # Set the row height for the content rows
        row_height = 0.5 * inch  # Adjust the value as needed
        table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEADING', (0, 0), (-1, -1), row_height),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))

        # Add the SPAN commands for the sessie.extra information
        for session_index in range(len(sessions)):
            i = 2 * session_index + 2
            table_style.add('SPAN', (0, i), (3, i))

        table.setStyle(table_style)

        # Add the table to the content
       

        fig, axs = plt.subplots(3, 1, figsize=(8, 16)) # Change figure size as needed

        # Plotting Inzicht
        # Create new figure for Inzicht plot
        fig, ax = plt.subplots()
        ax.plot(inzicht_data, label='Inzicht', color='#56b6ed', linewidth=2.0)
        ax.set_xlabel('Aantal sessies')
        ax.set_ylabel('Inzicht')
        ax.legend()
        imgdata = BytesIO()
        plt.savefig(imgdata, format='png')
        plt.clf()  # Clear figure
        imgdata.seek(0)
        reportlab_image_inzicht = Image(imgdata, width=300, height=300) # Change dimensions as needed
        content.append(reportlab_image_inzicht)

        # Create new figure for Kennis plot
        fig, ax = plt.subplots()
        ax.plot(kennis_data, label='Kennis', color='#56b6ed', linewidth=2.0)
        ax.set_xlabel('Aantal sessies')
        ax.set_ylabel('Kennis')
        ax.legend()
        imgdata = BytesIO()
        plt.savefig(imgdata, format='png')
        plt.clf()  # Clear figure
        imgdata.seek(0)
        reportlab_image_kennis = Image(imgdata, width=300, height=300) # Change dimensions as needed
        content.append(reportlab_image_kennis)

        # Create new figure for Werkhouding plot
        fig, ax = plt.subplots()
        ax.plot(werkhouding_data, label='Werkhouding', color='#56b6ed', linewidth=2.0)
        ax.set_xlabel('Aantal sessies')
        ax.set_ylabel('Werkhouding')
        ax.legend()
        imgdata = BytesIO()
        plt.savefig(imgdata, format='png')
        plt.clf()  # Clear figure
        imgdata.seek(0)
        reportlab_image_werkhouding = Image(imgdata, width=300, height=300) # Change dimensions as needed
        
        content.append(reportlab_image_werkhouding)
        content.append(table)
        # Build the PDF document
        doc.build(content)

        # Set the filename for the downloaded PDF
        filename = f"{student.naam}_{student.achternaam}_sessie_summary.pdf"

        # Set the buffer position to the start of the stream
        buffer.seek(0)

        # Return the PDF as a FileResponse with the appropriate headers
        return FileResponse(buffer, as_attachment=True, filename=filename)
    except Exception as e:
        return HttpResponseServerError(str(e))





    

def search_leerling(naam, achternaam):
    query = Q(naam__icontains=naam) & Q(achternaam__icontains=achternaam)
    leerling = Leerling.objects.filter(query).order_by('-naam', '-achternaam').first()
    
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
        




class SessieListView(LoginRequiredMixin, ListView):
    model = Sessie
    template_name = 'Login/sessie_detail.html'
    context_object_name = 'sessies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get current user
        user = self.request.user
        user_schools = School.objects.none()  # Start with no schools
      
        # Check if user is a Begeleider
        if hasattr(user, 'begeleider'):
            user_schools = user.begeleider.scholen.all() #type:ignore
            
        # Check if user is a Teamleider
        if hasattr(user, 'teamleider'):
            user_schools = School.objects.filter(id=user.teamleider.school.id) #type:ignore

        # If user is neither Begeleider nor Teamleider, return original context
        if not user_schools:
            return context

        models = ['Vak', 'Leerling', 'Niveau', 'Klas']

        for model in models:
            context[model.lower() + 's'] = globals()[model].objects.all()

        models2 = ['Begeleider', 'School']

        for model in models2:
            if model == 'Begeleider':
                # For Begeleiders, we filter by the schools related to the user
                context[model.lower() + 's'] = globals()[model].objects.filter(scholen__in=user_schools).distinct()
                
            elif model == 'School':
                # For Schools, we can directly use the user's schools
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

