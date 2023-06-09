from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import School, Niveau, Vak, Klas, Begeleider, Teamleider, Leerling, Materiaal, Sessie
from .forms import StudentForm, SessieForm, SessieFormUpdate, MateriaalForm, LoginForm
from .views import AddStudentView, DeleteMateriaalView, StudentDetailView, AddSessieView, SessieDetailView, StudentListView, SessieListView, DeleteSessieView, UpdateSessieView, AddMateriaalView, MateriaalListView, DeleteMateriaalView, UpdateMateriaalView, MateriaalDetailView, get, SessieListViewAPI, StudentListAPI, add_sessie_view



class AddStudentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('Login:add_student')

        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_add_student_post(self):
        # Log in
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.url, {
            'naam': 'Test',
            'achternaam': 'Test',
            'email': 'test@example.com',
            'school': 1,  # Change to the ID of an existing School object in your database
            'klas': 1,    # Change to the ID of an existing Klas object in your database
            'niveau': 1   # Change to the ID of an existing Niveau object in your database
        })

        self.assertEqual(response.status_code, 200)

        # Update the expected redirect URL to 'student_all' after successful addition of a student
        self.assertRedirects(response, reverse('Login:student_all'))  # Replace with your expected redirect URL

