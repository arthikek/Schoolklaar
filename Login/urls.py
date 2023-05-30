from django.urls import path
from .views import AddStudentView, DeleteMateriaalView, StudentDetailView, AddSessieView, SessieDetailView, StudentListView, SessieListView, DeleteSessieView, UpdateSessieView, AddMateriaalView,MateriaalListView, DeleteMateriaalView, UpdateMateriaalView,MateriaalDetailView,get, SessieListViewAPI, StudentListAPI
app_name='Login'

urlpatterns = [
    # Student related urls
    path('add_student/', AddStudentView.as_view(), name='add_student'),
    path('student_all/', StudentListView.as_view(), name='student_all'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),

    # Sessie related urls
    path('', AddSessieView.as_view(), name='home'),
    path('add_sessie/', AddSessieView.as_view(), name='add_sessie'),
    path('sessie_all/', SessieListView.as_view(), name='sessie_all'),
    path('sessie/<int:pk>/', SessieDetailView.as_view(), name='sessie_detail'),
    path('sessie/<int:pk>/update/', UpdateSessieView.as_view(), name='sessie_update'),
    path('sessie/<int:pk>/delete/', DeleteSessieView.as_view(), name='sessie_delete'),

    # Materiaal related urls
    path('add_materiaal/', AddMateriaalView.as_view(), name='add_materiaal'),
    path('material_all/', MateriaalListView.as_view(), name='materiaal_all'),
    path('materiaal/<int:pk>/', MateriaalDetailView.as_view(), name='materiaal_detail'),
    path('materiaal/<int:pk>/delete/', DeleteMateriaalView.as_view(), name='materiaal_delete'),
    path('materiaal/<int:pk>/update/', UpdateMateriaalView.as_view(), name='materiaal_update'),
    path('materiaal/<int:pk>/download/', get, name='materiaal_download'),  # new URL for downloading a Materiaal
    
    #api
    path('api/sessie/', SessieListViewAPI.as_view(), name='api_sessie'),
    path('api/student/', StudentListAPI.as_view(), name='api_student')
    
]


