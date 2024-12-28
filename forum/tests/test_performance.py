import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Sujet

class ForumPerformanceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.sujet = Sujet.objects.create(
            user=self.user,
            question="Performance question?",
            titre="Performance sujet"
        )

    def test_forum_list_performance(self):
        """Test de performance pour la liste des forums"""
        start_time = time.time()
        response = self.client.get(reverse('forum'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)  # Temps de réponse < 500 ms
