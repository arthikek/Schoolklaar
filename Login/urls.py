from django.urls import path
from .views import AddStudentView, StudentDetailView, AddSessieView, SessieDetailView, StudentListView, SessieListView, DeleteSessieView, UpdateSessieView, AddMateriaalView 

app_name='Login'

urlpatterns = [
    path('', AddSessieView.as_view(), name='home'),
    path('add_student/', AddStudentView.as_view(), name='add_student'),
    path('add_sessie/', AddSessieView.as_view(), name='add_sessie'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('sessie/<int:pk>/', SessieDetailView.as_view(), name='sessie_detail'),
    path('student_all/', StudentListView.as_view(), name='student_all'),
    path('sessie_all/', SessieListView.as_view(), name='sessie_all'),
    path('sessie/<int:pk>/update/', UpdateSessieView.as_view(), name='sessie_update'),
    path('sessie/<int:pk>/delete/', DeleteSessieView.as_view(), name='sessie_delete'),
    path('add_materiaal/', AddMateriaalView.as_view(), name='add_materiaal'),  # Add a trailing slash to the URL
]