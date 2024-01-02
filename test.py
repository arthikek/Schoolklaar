from django.test import TestCase
from Login.models import School, Niveau, Leerling, User
from django.conf import settings
import os

class EnvironmentVariablesTest(TestCase):
    def test_environment_variables(self):
        # Assert that DATABASE_TYPE is set
        self.assertTrue('DATABASE_TYPE' in os.environ)

        # Assert that other environment variables are set
        self.assertTrue('DB_NAME' in os.environ)
        self.assertTrue('DB_USER' in os.environ)
        self.assertTrue('DB_PASSWORD' in os.environ)
        self.assertTrue('DB_HOST' in os.environ)
        self.assertTrue('DB_PORT' in os.environ)

        # Print additional information
        print("== Environment Variables Test ==")
        print("Environment variables are set correctly.\n")

class DatabaseTypeTest(TestCase):
    def test_database_backend(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.postgresql_psycopg2')

        # Print additional information
        print("== Database Type Test ==")
        print("Database backend is correctly configured.\n")

class SchoolTestCase(TestCase):
    def setUp(self):
        School.objects.create(naam="Test School", grootte=500 ,secret_code="f2AjB9")

    def test_school_creation(self):
        school = School.objects.get(naam="Test School")
        self.assertEqual(school.grootte, 500)

        # Print additional information
        print("== School Creation Test ==")
        print("School creation test passed.\n")

class NiveauTestCase(TestCase):
    def setUp(self):
        school = School.objects.create(naam="Test School", grootte=500, secret_code="f2AjB8")
        niveau = Niveau.objects.create(naam="Test Niveau")
        niveau.scholen.set([school])

    def test_niveau_creation(self):
        niveau = Niveau.objects.get(naam="Test Niveau")
        self.assertEqual(niveau.scholen.count(), 1)

        # Print additional information
        print("== Niveau Creation Test ==")
        print("Niveau creation test passed.\n")

class LeerlingTestCase(TestCase):
    def setUp(self):
        school = School.objects.create(naam="Test School", grootte=500 ,secret_code="f2AjB9")
        user = User.objects.create(username="testuser")
        Leerling.objects.create(naam="Test", achternaam="Leerling", email="test@example.com", school=school, gebruiker=user)

    def test_leerling_creation(self):
        leerling = Leerling.objects.get(naam="Test")
        self.assertEqual(leerling.achternaam, "Leerling")
        self.assertEqual(leerling.school.naam, "Test School")

        # Print additional information
        print("== Leerling Creation Test ==")
        print("Leerling creation test passed.\n")
