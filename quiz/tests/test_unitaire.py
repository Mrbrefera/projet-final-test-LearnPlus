from django.test import TestCase
from django.contrib.auth.models import User
from quiz.models import Quiz, Devoir, Question, Reponse, QuizResult, QuestionResponse
from school.models import Chapitre

class QuizModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testinstructor', password='password123')
        self.student = User.objects.create_user(username='teststudent', password='password123')
        self.quiz = Quiz.objects.create(
            instructor=self.user,
            titre="Test Quiz",
            temps=45
        )
        self.chapitre = Chapitre.objects.create(titre="Chapitre 1", description="Introduction")
        self.devoir = Devoir.objects.create(
            sujet="Test Devoir",
            dateDebut="2024-12-25 10:00:00",
            dateFermeture="2024-12-30 10:00:00",
            chapitre=self.chapitre,
            coefficient=3,
            support="path/to/support.pdf"
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            title="Question 1",
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
        self.quiz_result = QuizResult.objects.create(
            student=self.student,
            quiz=self.quiz,
            score=90,
            total_questions=10,
            correct_answers=9,
            completion_time=300
        )
        self.question_response = QuestionResponse.objects.create(
            quiz_result=self.quiz_result,
            question=self.question,
            selected_answer="Option B",
            is_correct=True
        )

    def test_multiple_questions_in_quiz(self):
        """Vérifie que plusieurs questions peuvent être ajoutées à un quiz"""
        Question.objects.create(quiz=self.quiz, title="Question 2", question_type="qcm", score=10)
        self.assertEqual(self.quiz.questions.count(), 2)

    def test_correct_answer(self):
        """Vérifie que la réponse correcte est bien identifiée"""
        self.assertTrue(self.reponse2.is_True)
        self.assertFalse(self.reponse1.is_True)

    def test_question_response_association(self):
        """Vérifie que la réponse à une question est bien associée au quiz"""
        self.assertEqual(self.question_response.selected_answer, "Option B")
        self.assertTrue(self.question_response.is_correct)

    def test_quiz_score_calculation(self):
        """Vérifie que le score total d'un quiz est correct"""
        self.assertEqual(self.quiz_result.score, 90)

    def test_quiz_result_string_representation(self):
        """Vérifie la représentation en chaîne des résultats d'un quiz"""
        self.assertEqual(str(self.quiz_result), "teststudent - Test Quiz - 90.0%")

    def test_quiz_absolute_url(self):
        """Vérifie que l'URL absolue d'un résultat de quiz est correcte"""
        self.assertEqual(self.quiz_result.get_absolute_url(), f"/quiz/results/{self.quiz_result.id}/")
