from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse
from school.models import Cours

class ForumFunctionalTest(TestCase):

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
        self.reponse = Reponse.objects.create(
            user=self.user,
            sujet=self.sujet,
            reponse="Voici une solution potentielle."
        )

    def test_sujet_creation_view(self):
        """Test la vue de création de sujet"""
        response = self.client.post(reverse('forum_ask'), {
            'titre': 'Nouveau sujet',
            'question': 'Nouvelle question',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Sujet.objects.filter(titre="Nouveau sujet").exists())

    def test_reponse_creation_view(self):
        """Test la vue de création de réponse"""
        response = self.client.post(reverse('forum_thread', args=[self.sujet.slug]), {
            'reponse': 'Nouvelle réponse',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reponse.objects.filter(reponse="Nouvelle réponse").exists())

    def test_forum_list_view(self):
        """Test la vue de liste des forums"""
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Problème mathématique")

    def test_thread_detail_view(self):
        """Test la vue détaillée d'un sujet"""
        response = self.client.get(reverse('forum_thread', args=[self.sujet.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quelle est la solution de ce problème ?")
