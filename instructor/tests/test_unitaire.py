from django.test import TestCase
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Matiere

class InstructorModelTest(TestCase):

    def setUp(self):
        # Création des données initiales pour les tests
        self.user = User.objects.create_user(username='testinstructor', password='password123')
        self.matiere1 = Matiere.objects.create(title="Mathématiques", description="Cours de maths avancés")
        self.matiere2 = Matiere.objects.create(title="Physique", description="Cours de physique appliquée")
        self.instructor = Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Rue des Tests",
            bio="Bio de test"
        )
        self.instructor.matieres.set([self.matiere1, self.matiere2])

    def test_instructor_creation(self):
        """Vérifie que l'instructeur est créé correctement"""
        self.assertEqual(self.instructor.user.username, "testinstructor")
        self.assertEqual(self.instructor.contact, "123456789")
        self.assertEqual(self.instructor.bio, "Bio de test")

    def test_slug_generation(self):
        """Vérifie que le slug est généré automatiquement"""
        self.instructor.save()
        self.assertEqual(self.instructor.slug, "testinstructor")

    def test_instructor_matiere_relation(self):
        """Vérifie que les matières sont correctement associées"""
        self.assertEqual(self.instructor.matieres.count(), 2)
        self.assertIn(self.matiere1, self.instructor.matieres.all())
        self.assertIn(self.matiere2, self.instructor.matieres.all())

    def test_instructor_get_u_type(self):
        """Test de la méthode get_u_type"""
        self.assertTrue(self.instructor.get_u_type)

    def test_update_contact_information(self):
        """Vérifie la mise à jour des informations de contact"""
        self.instructor.contact = "987654321"
        self.instructor.save()
        self.assertEqual(self.instructor.contact, "987654321")

    def test_update_bio(self):
        """Vérifie la mise à jour de la biographie"""
        self.instructor.bio = "Nouvelle bio de test"
        self.instructor.save()
        self.assertEqual(self.instructor.bio, "Nouvelle bio de test")

    def test_remove_matiere(self):
        """Vérifie la suppression d'une matière associée"""
        self.instructor.matieres.remove(self.matiere1)
        self.assertEqual(self.instructor.matieres.count(), 1)
        self.assertNotIn(self.matiere1, self.instructor.matieres.all())

    def test_add_matiere(self):
        """Vérifie l'ajout d'une nouvelle matière"""
        matiere3 = Matiere.objects.create(title="Chimie", description="Cours de chimie")
        self.instructor.matieres.add(matiere3)
        self.assertEqual(self.instructor.matieres.count(), 3)
        self.assertIn(matiere3, self.instructor.matieres.all())

    def test_delete_instructor(self):
        """Vérifie la suppression d'un instructeur"""
        instructor_id = self.instructor.id
        self.instructor.delete()
        with self.assertRaises(Instructor.DoesNotExist):
            Instructor.objects.get(id=instructor_id)

    def test_instructor_string_representation(self):
        """Vérifie la représentation en chaîne de l'instructeur"""
        self.assertEqual(str(self.instructor), self.user.username)
