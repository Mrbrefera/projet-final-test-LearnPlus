from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from quiz.models import Quiz, Question, Reponse

class QuizFunctionalTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testinstructor', password='password123')
        self.client.login(username='testinstructor', password='password123')
        self.quiz = Quiz.objects.create(
            instructor=self.user,
            titre="Functional Test Quiz",
            temps=60
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            title="Functional Test Question",
            question_type="qcm",
            score=5
        )
        self.reponse1 = Reponse.objects.create(
            question=self.question,
            reponse="Option A",
            is_True=False
        )
        self.reponse2 = Reponse.objects.create(
            question=self.question,
            reponse="Option B",
            is_True=True
        )

    def test_quiz_creation_view(self):
        """Test de la vue de création d'un quiz"""
        response = self.client.post(reverse('quiz-add'), {
            'titre': 'New Quiz',
            'temps': 30
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Quiz.objects.filter(titre="New Quiz").exists())

    def test_add_question_to_quiz(self):
        """Test de l'ajout de questions à un quiz"""
        response = self.client.post(reverse('quiz-question-add', args=[self.quiz.id]), {
            'title': 'Question 2',
            'question_type': 'qcm',
            'score': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Question.objects.filter(title="Question 2").exists())
