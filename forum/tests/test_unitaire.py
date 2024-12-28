from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse
from school.models import Cours

class ForumModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
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

    def test_sujet_creation(self):
        """Vérifie la création d'un sujet"""
        self.assertEqual(self.sujet.user.username, "testuser")
        self.assertEqual(self.sujet.titre, "Problème mathématique")
        self.assertEqual(self.sujet.question, "Quelle est la solution de ce problème ?")

    def test_reponse_creation(self):
        """Vérifie la création d'une réponse"""
        self.assertEqual(self.reponse.user.username, "testuser")
        self.assertEqual(self.reponse.reponse, "Voici une solution potentielle.")
        self.assertEqual(self.reponse.sujet, self.sujet)

    def test_slug_sujet(self):
        """Vérifie la génération automatique du slug pour un sujet"""
        self.assertIn("probleme-mathematique", self.sujet.slug)

    def test_slug_reponse(self):
        """Vérifie la génération automatique du slug pour une réponse"""
        self.assertIn("probleme-mathematique", self.reponse.slug)

    def test_update_sujet(self):
        """Vérifie la mise à jour des informations d'un sujet"""
        self.sujet.titre = "Nouveau titre"
        self.sujet.save()
        self.assertEqual(self.sujet.titre, "Nouveau titre")

    def test_update_reponse(self):
        """Vérifie la mise à jour des informations d'une réponse"""
        self.reponse.reponse = "Nouvelle solution"
        self.reponse.save()
        self.assertEqual(self.reponse.reponse, "Nouvelle solution")

    def test_delete_sujet(self):
        """Vérifie la suppression d'un sujet"""
        sujet_id = self.sujet.id
        self.sujet.delete()
        with self.assertRaises(Sujet.DoesNotExist):
            Sujet.objects.get(id=sujet_id)

    def test_delete_reponse(self):
        """Vérifie la suppression d'une réponse"""
        reponse_id = self.reponse.id
        self.reponse.delete()
        with self.assertRaises(Reponse.DoesNotExist):
            Reponse.objects.get(id=reponse_id)

    def test_string_representation_sujet(self):
        """Vérifie la représentation en chaîne du modèle Sujet"""
        self.assertEqual(str(self.sujet), "Problème mathématique")

    def test_string_representation_reponse(self):
        """Vérifie la représentation en chaîne du modèle Reponse"""
        self.assertEqual(str(self.reponse), "Problème mathématique")
