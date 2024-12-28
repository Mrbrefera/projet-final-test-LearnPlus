from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from student.models import Student, StudentReponse
from school.models import Classe, Niveau, Filiere

class StudentIntegrationTest(TestCase):

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

    def test_student_quiz_integration(self):
        """Test d'intégration entre étudiant et liste des quiz"""
        response = self.client.get(reverse('quiz-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz")

    def test_student_class_integration(self):
        """Test d'intégration entre Student et Classe"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sciences")
        self.assertContains(response, "Terminale 1")
