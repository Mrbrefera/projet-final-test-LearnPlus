import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from student.models import Student
from school.models import Classe, Niveau, Filiere

class StudentPerformanceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="teststudent", password="password123")
        self.filiere = Filiere.objects.create(nom="Sciences")
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1, filiere=self.filiere)
        self.student = Student.objects.create(
            user=self.user,
            classe=self.classe,
            bio="Bio test",
            photo="path/to/photo.jpg"
        )
        self.client.login(username="teststudent", password="password123")

    def test_dashboard_performance(self):
        """Test de performance pour la vue dashboard"""
        start_time = time.time()
        response = self.client.get(reverse('index_student'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_profile_performance(self):
        """Test de performance pour la vue profil"""
        start_time = time.time()
        response = self.client.get(reverse('profile'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)
