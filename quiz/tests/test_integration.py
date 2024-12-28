from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from quiz.models import Quiz, Question, Reponse

class QuizIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testinstructor', password='password123')
        self.quiz = Quiz.objects.create(
            instructor=self.user,
            titre="Integration Test Quiz",
            temps=40
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            title="Integration Test Question",
            question_type="qcm",
            score=5
        )
        self.reponse = Reponse.objects.create(
            question=self.question,
            reponse="Integration Test Answer",
            is_True=True
        )

    def test_quiz_question_integration(self):
        """Test d'intégration entre Quiz, Questions et Réponses"""
        response = self.client.get(reverse('quiz-detail', args=[self.quiz.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Integration Test Question")
        self.assertContains(response, "Integration Test Answer")
