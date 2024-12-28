from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Matiere, Chapitre, Cours

class InstructorIntegrationTest(TestCase):

    def setUp(self):
        # Configuration initiale des données
        self.user = User.objects.create_user(username='testinstructor', password='password123')
        self.instructor = Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Integration Street",
            bio="Integration bio"
        )
        self.matiere = Matiere.objects.create(title="Mathématiques", description="Cours de maths")
        self.chapitre = Chapitre.objects.create(
            titre="Chapitre 1",
            matiere=self.matiere,
            classe=None,  # Ajoutez une classe si nécessaire
            description="Description du chapitre 1",
            status=True
        )
        self.cours = Cours.objects.create(
            titre="Cours 1",
            chapitre=self.chapitre,
            description="Description du cours 1",
            status=True
        )
        self.instructor.matieres.add(self.matiere)
        self.client.login(username='testinstructor', password='password123')

    def test_dashboard_display_matiere(self):
        """Test d'intégration entre Instructor et Matiere pour l'affichage sur le dashboard"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathématiques")

    def test_dashboard_display_chapitre(self):
        """Test d'intégration entre Matiere et Chapitre pour l'affichage sur le dashboard"""
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "Chapitre 1")

    def test_dashboard_display_cours(self):
        """Test d'intégration entre Chapitre et Cours pour l'affichage sur le dashboard"""
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "Cours 1")

    def test_course_add_integration(self):
        """Test d'intégration pour l'ajout d'un cours"""
        response = self.client.post(reverse('instructor-course-add'), {
            'titre': 'Cours 2',
            'description': 'Description du cours 2',
            'chapitre': self.chapitre.id,
        })
        self.assertEqual(response.status_code, 200)  # Vérifiez que la vue retourne un succès
        self.assertTrue(Cours.objects.filter(titre="Cours 2").exists())

    def test_chapitre_creation_integration(self):
        """Test d'intégration pour l'ajout d'un chapitre"""
        response = self.client.post(reverse('lesson_add', args=[self.matiere.slug]), {
            'titre': 'Chapitre 2',
            'description': 'Description du chapitre 2',
            'matiere': self.matiere.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Chapitre.objects.filter(titre="Chapitre 2").exists())

    def test_quiz_creation_integration(self):
        """Test d'intégration pour la création d'un quiz"""
        response = self.client.post(reverse('quiz_add'), {
            'titre': 'Quiz 1',
            'matiere': self.matiere.id,
            'temps': 30,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiz créé avec succès")

    def test_instructor_profile_update(self):
        """Test d'intégration pour la mise à jour du profil de l'instructeur"""
        response = self.client.post(reverse('profile'), {
            'bio': 'Nouvelle bio',
            'contact': '000000000',
            'adresse': 'New Address',
        })
        self.instructor.refresh_from_db()
        self.assertEqual(self.instructor.bio, 'Nouvelle bio')
        self.assertEqual(self.instructor.contact, '000000000')

    def test_forum_creation_integration(self):
        """Test d'intégration pour la création d'un forum"""
        response = self.client.post(reverse('forum_ask'), {
            'titre': 'Forum Test',
            'question': 'Quelle est la meilleure méthode ?',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Votre sujet a bien été ajouté!")

    def test_quiz_display_questions(self):
        """Test d'intégration pour afficher les questions d'un quiz"""
        response = self.client.get(reverse('quiz_edit', args=[1]))  # Assurez-vous d'avoir un quiz avec ID 1
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathématiques")  # Vérifie que la matière liée au quiz est affichée

    def test_messages_integration(self):
        """Test d'intégration pour l'accès aux messages"""
        response = self.client.get(reverse('instructor-messages', args=[self.instructor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Messages")
