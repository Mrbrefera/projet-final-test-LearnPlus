from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe

class ChatModelTest(TestCase):

    def setUp(self):
        # Création des données initiales
        self.classe = Classe.objects.create(nom="Classe A", niveau="Terminale")
        self.salon = Salon.objects.create(nom="Salon Classe A", classe=self.classe)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.message = Message.objects.create(
            auteur=self.user,
            message="Bonjour, ceci est un message.",
            salon=self.salon
        )

    def test_salon_creation(self):
        """Vérifie la création d'un salon"""
        self.assertEqual(self.salon.nom, "Salon Classe A")
        self.assertEqual(self.salon.classe, self.classe)

    def test_message_creation(self):
        """Vérifie la création d'un message"""
        self.assertEqual(self.message.auteur.username, "testuser")
        self.assertEqual(self.message.message, "Bonjour, ceci est un message.")
        self.assertEqual(self.message.salon, self.salon)

    def test_salon_string_representation(self):
        """Vérifie la représentation en chaîne d'un salon"""
        self.assertEqual(str(self.salon), "Salon Classe A")

    def test_message_string_representation(self):
        """Vérifie la représentation en chaîne d'un message"""
        self.assertEqual(str(self.message), "testuser")

    def test_update_salon_name(self):
        """Vérifie la mise à jour du nom d'un salon"""
        self.salon.nom = "Nouveau Salon"
        self.salon.save()
        self.assertEqual(self.salon.nom, "Nouveau Salon")

    def test_update_message_content(self):
        """Vérifie la mise à jour du contenu d'un message"""
        self.message.message = "Message modifié"
        self.message.save()
        self.assertEqual(self.message.message, "Message modifié")

    def test_delete_salon(self):
        """Vérifie la suppression d'un salon"""
        salon_id = self.salon.id
        self.salon.delete()
        with self.assertRaises(Salon.DoesNotExist):
            Salon.objects.get(id=salon_id)

    def test_delete_message(self):
        """Vérifie la suppression d'un message"""
        message_id = self.message.id
        self.message.delete()
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=message_id)
