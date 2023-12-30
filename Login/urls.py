from django.urls import path





from .views.Instructor.instructor_sessie_view import AddSessieAPIView, AddSessieAPIView_2,  UpdateSessieAPIView
from.views.Instructor.instructor_student_view import AddStudentAPIView
from.views.Instructor.instructor_material_view import MateriaalListApiView, IndividualMateriaalListApiView, CreateMateriaalAPIView
from .views.Instructor.instructor_helpers_view import GeneralContextAPIView


from .views.Student.student_sessie_view import SessieListViewAPI 
from .views.Student.student_student_view import StudentListAPI, StudentDetailAPI
from.views.Student.student_helpers_view import create_rating, create_leerling_with_secret_code, check_leerling_status, get_all_subjects



app_name='Login'

urlpatterns = [


    #api Student Portal
    path('api/sessie/', SessieListViewAPI.as_view(), name='api_sessie'),
    path('api/student/', StudentListAPI.as_view(), name='api_student'),     #What kind of view is this? Is this safe?
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


