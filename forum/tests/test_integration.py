from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse
from school.models import Cours

class ForumIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.cours = Cours.objects.create(titre="Mathématiques", description="Cours de maths")
        self.sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            question="Quelle est la solution de ce problème ?",
            titre="Problème mathématique"
        )

    def test_sujet_reponse_integration(self):
        """Test d'intégration entre Sujet et Reponse"""
        response = self.client.post(reverse('forum_thread', args=[self.sujet.slug]), {
            'reponse': 'Nouvelle réponse intégrée',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reponse.objects.filter(reponse="Nouvelle réponse intégrée").exists())
