from django.test import TestCase
from django.contrib.auth.models import User
from student.models import Student, StudentReponse
from school.models import Classe, Niveau, Filiere

class StudentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="teststudent", password="password123")
        self.filiere = Filiere.objects.create(nom="Sciences")
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1, filiere=self.filiere)
        self.student = Student.objects.create(
            user=self.user,
            classe=self.classe,
            bio="Bio test",
            photo="path/to/photo.jpg"
        )

    def test_student_creation(self):
        """Test de création d'un étudiant"""
        self.assertEqual(self.student.user.username, "teststudent")
        self.assertEqual(self.student.bio, "Bio test")
        self.assertEqual(self.student.classe, self.classe)

    def test_student_update(self):
        """Test de mise à jour d'un étudiant"""
        self.student.bio = "Updated bio"
        self.student.save()
        self.assertEqual(self.student.bio, "Updated bio")

    def test_student_delete(self):
        """Test de suppression d'un étudiant"""
        self.student.delete()
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())

    def test_student_class_relation(self):
        """Test de relation entre étudiant et classe"""
        self.assertEqual(self.student.classe.filiere.nom, "Sciences")
        self.assertEqual(self.student.classe.niveau.nom, "Terminale")

    def test_slug_generation(self):
        """Test de génération automatique de slug"""
        self.assertEqual(self.student.slug, "teststudent")

    def test_get_u_type_property(self):
        """Test de la propriété get_u_type"""
        self.assertTrue(self.student.get_u_type)

    def test_student_reponse_creation(self):
        """Test de création d'une réponse d'étudiant"""
        response = StudentReponse.objects.create(
            student=self.student,
            question="Quelle est la capitale de la France ?",
            reponse="Paris"
        )
        self.assertEqual(response.student, self.student)
        self.assertEqual(response.question, "Quelle est la capitale de la France ?")
        self.assertEqual(response.reponse, "Paris")

    def test_student_reponse_update(self):
        """Test de mise à jour d'une réponse d'étudiant"""
        response = StudentReponse.objects.create(
            student=self.student,
            question="Quelle est la capitale de la France ?",
            reponse="Paris"
        )
        response.reponse = "Londres"
        response.save()
        self.assertEqual(response.reponse, "Londres")

    def test_student_reponse_delete(self):
        """Test de suppression d'une réponse d'étudiant"""
        response = StudentReponse.objects.create(
            student=self.student,
            question="Quelle est la capitale de la France ?",
            reponse="Paris"
        )
        response.delete()
        self.assertFalse(StudentReponse.objects.filter(id=response.id).exists())
