from django.urls import path
from .views import (AddStudentView, DeleteMateriaalView, StudentDetailView, AddSessieView, SessieDetailView, StudentDetailView_2, 
                    StudentListView, SessieListView, DeleteSessieView, UpdateSessieView, AddMateriaalView, 
                    MateriaalListView, UpdateMateriaalView, MateriaalDetailView, get, SessieListViewAPI, 
                    StudentListAPI, add_sessie_view,  StudentDetailView_2,StudentDetailAPI,create_rating)




app_name='Login'

urlpatterns = [
    # Student related urls
    path('add_student/', AddStudentView.as_view(), name='add_student'),
    path('student_all/', StudentListView.as_view(), name='student_all'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/report/<int:pk>', StudentDetailView_2.as_view(), name='student_detail_2'),

    # Sessie related urls
    path('', AddSessieView.as_view(), name='home'),
    path('add_sessie/', AddSessieView.as_view(), name='add_sessie'),
    path('sessie_all/', SessieListView.as_view(), name='sessie_all'),
    path('sessie/<int:pk>/', SessieDetailView.as_view(), name='sessie_detail'),
    path('sessie/<int:pk>/update/', UpdateSessieView.as_view(), name='sessie_update'),
    path('sessie/<int:pk>/delete/', DeleteSessieView.as_view(), name='sessie_delete'),
    

    # Materiaal related urls
    path('add_materiaal/', AddMateriaalView.as_view(), name='add_materiaal'),
    path('materiaal_all/', MateriaalListView.as_view(), name='materiaal_all'),
    path('materiaal/<int:pk>/', MateriaalDetailView.as_view(), name='materiaal_detail'),
    path('materiaal/<int:pk>/delete/', DeleteMateriaalView.as_view(), name='materiaal_delete'),
    path('materiaal/<int:pk>/update/', UpdateMateriaalView.as_view(), name='materiaal_update'),
    path('materiaal/<int:pk>/download/', get, name='materiaal_download'),  

    #api
    path('api/sessie/', SessieListViewAPI.as_view(), name='api_sessie'),
    path('api/student/', StudentListAPI.as_view(), name='api_student'),
    path('api/student_detail/', StudentDetailAPI.as_view(), name='api_student_detail'),
    path('api/create_rating/', create_rating, name='api_create_rating'),
    #form
    path('form/', add_sessie_view, name='form'),

]


