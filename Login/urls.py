from django.urls import path

from .views_old import (AddSessieAPIView_2, SessieListViewAPI,  
                    AddStudentAPIView, MateriaalListApiView, IndividualMateriaalListApiView, 
                    StudentListAPI,   StudentDetailAPI,create_rating, get_all_subjects, GeneralContextAPIView,CreateMateriaalAPIView,UpdateSessieAPIView,create_leerling_with_secret_code,check_leerling_status) 



from .views.sessie import *




app_name='Login'

urlpatterns = [


    #api Student Portal
    path('api/sessie/', SessieListViewAPI.as_view(), name='api_sessie'),
    path('api/student/', StudentListAPI.as_view(), name='api_student'),
    path('api/student_detail/', StudentDetailAPI.as_view(), name='api_student_detail'),
    path('api/student_detail/<int:pk>/', StudentDetailAPI.as_view(), name='student-detail-by-pk'),
    path('api/create_rating/', create_rating, name='api_create_rating'),
    path('api/vakken/', get_all_subjects, name='api_get_all_subjects'),
    path('api/create_leerling/', create_leerling_with_secret_code, name='api_create_leerling_with_secret_code'),
     path('api/check_leerling_status/', check_leerling_status, name='check-leerling-status'),


    #api Instructor Portal
    path('api/add_sessie/', AddSessieAPIView.as_view(), name='api_add_sessie'),
    path('api/add_sessie_2/', AddSessieAPIView_2.as_view(), name='api_add_sessie_2'),
    path('api/add_student/', AddStudentAPIView.as_view(), name='api_add_student'),
    path('api/general_context/', GeneralContextAPIView.as_view(), name='api_general_context'),
    path('api/materiaal_all/', MateriaalListApiView.as_view(), name='api_materiaal_all_context'),
    path('api/materiaal_ind/', IndividualMateriaalListApiView.as_view(), name='api_materiaal_all_context'),
    path('api/add_materiaal/', CreateMateriaalAPIView.as_view(), name='api_add_materiaal'),
    path('api/sessies/<int:sessie_id>/', UpdateSessieAPIView.as_view(), name='update_sessie'),



  

]


