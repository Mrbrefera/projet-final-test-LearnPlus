import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Matiere

class PerformanceTest(TestCase):

    def setUp(self):
        # Configuration initiale
        self.user = User.objects.create_user(username='testinstructor', password='password123')
        self.instructor = Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Test Street",
            bio="Test bio"
        )
        self.matiere = Matiere.objects.create(title="Mathématiques", description="Cours de maths")
        self.instructor.matieres.add(self.matiere)
        self.client.login(username='testinstructor', password='password123')

    def test_dashboard_performance(self):
        """Test de performance pour la vue tableau de bord"""
        start_time = time.time()
        response = self.client.get(reverse('dashboard'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)  # Temps de réponse < 500 ms

    def test_profile_performance(self):
        """Test de performance pour la vue profil"""
        start_time = time.time()
        response = self.client.get(reverse('profile'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_course_add_performance(self):
        """Test de performance pour la vue d'ajout de cours"""
        start_time = time.time()
        response = self.client.get(reverse('instructor-course-add'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_quiz_add_performance(self):
        """Test de performance pour la vue d'ajout de quiz"""
        start_time = time.time()
        response = self.client.get(reverse('quiz_add'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_forum_performance(self):
        """Test de performance pour la vue forum"""
        start_time = time.time()
        response = self.client.get(reverse('forum'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_messages_performance(self):
        """Test de performance pour la vue messages"""
        start_time = time.time()
        response = self.client.get(reverse('instructor-messages', args=[self.instructor.id]))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_chapitre_add_performance(self):
        """Test de performance pour l'ajout de chapitre"""
        start_time = time.time()
        response = self.client.post(reverse('lesson_add', args=['test-slug']), {
            'titre': 'Chapitre Performance',
            'description': 'Description du chapitre',
            'matiere': self.matiere.id,
        })
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_cours_list_performance(self):
        """Test de performance pour la liste des cours"""
        start_time = time.time()
        response = self.client.get(reverse('instructor-courses'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_quiz_edit_performance(self):
        """Test de performance pour la modification de quiz"""
        start_time = time.time()
        response = self.client.get(reverse('quiz_edit', args=[1]))  # Assurez-vous qu'un quiz avec ID 1 existe
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_earnings_performance(self):
        """Test de performance pour la vue revenus"""
        start_time = time.time()
        response = self.client.get(reverse('earnings'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)
