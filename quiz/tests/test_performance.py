import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from quiz.models import Quiz

class QuizPerformanceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.quiz = Quiz.objects.create(
            instructor=self.user,
            titre="Performance Test Quiz",
            temps=30
        )

    def test_quiz_detail_performance(self):
        """Test de performance pour la vue détaillée d'un quiz"""
        start_time = time.time()
        response = self.client.get(reverse('quiz-detail', args=[self.quiz.slug]))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)  # Temps de réponse < 500 ms
