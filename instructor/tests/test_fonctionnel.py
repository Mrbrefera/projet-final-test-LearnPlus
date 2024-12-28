from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Matiere

class InstructorFunctionalTest(TestCase):

    def setUp(self):
        # Configuration initiale des données pour les tests
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

    def test_dashboard_view(self):
        """Test l'accès au tableau de bord instructeur"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathématiques")
        self.assertTemplateUsed(response, 'pages/instructor-dashboard.html')

    def test_course_add_view(self):
        """Test l'accès à la vue d'ajout de cours"""
        response = self.client.get(reverse('instructor-course-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-course-add.html')

    def test_profile_edit_view(self):
        """Test l'accès à la vue de modification du profil"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test bio")
        self.assertTemplateUsed(response, 'pages/instructor-profile.html')

    def test_view_courses(self):
        """Test l'accès à la liste des cours de l'instructeur"""
        response = self.client.get(reverse('instructor-courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathématiques")
        self.assertTemplateUsed(response, 'pages/instructor-courses.html')

    def test_add_quiz_view(self):
        """Test l'accès à la vue d'ajout de quiz"""
        response = self.client.get(reverse('quiz_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-quiz-add.html')

    def test_edit_quiz_view(self):
        """Test l'accès à la vue de modification d'un quiz"""
        # Remplacez 1 par l'ID d'un quiz existant dans votre application
        response = self.client.get(reverse('quiz_edit', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-quiz-edit.html')

    def test_forum_view(self):
        """Test l'accès au forum instructeur"""
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-forum.html')

    def test_messages_view(self):
        """Test l'accès à la page des messages"""
        response = self.client.get(reverse('instructor-messages', args=[self.instructor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-messages.html')

    def test_add_lesson_view(self):
        """Test l'accès à la vue d'ajout de leçons"""
        # Remplacez 'test-slug' par un slug valide dans votre application
        response = self.client.get(reverse('lesson_add', args=['test-slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-lesson-add.html')

    def test_earnings_view(self):
        """Test l'accès à la vue des revenus"""
        response = self.client.get(reverse('earnings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/instructor-account-edit.html')

