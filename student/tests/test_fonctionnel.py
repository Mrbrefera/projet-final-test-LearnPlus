from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from student.models import Student
from school.models import Classe, Niveau, Filiere

class StudentFunctionalTest(TestCase):

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

    def test_dashboard_view(self):
        """Test de la vue dashboard pour les étudiants"""
        response = self.client.get(reverse('index_student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/fixed-student-dashboard.html')

    def test_profile_view(self):
        """Test de la vue profile"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/fixed-student-profile.html')

    def test_quiz_list_view(self):
        """Test de la vue liste des quiz"""
        response = self.client.get(reverse('quiz-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/fixed-student-quiz-list.html')

    def test_course_list_view(self):
        """Test de la vue liste des cours"""
        response = self.client.get(reverse('my_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/fixed-student-my-courses.html')

    def test_payment_view(self):
        """Test de la vue paiement"""
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/fixed-student-account-billing-payment-information.html')

    def test_invalid_page_access(self):
        """Test de tentative d'accès à une page non autorisée"""
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('login') + '?next=/student/profile/')
