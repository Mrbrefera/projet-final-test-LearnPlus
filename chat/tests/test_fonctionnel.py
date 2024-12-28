from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe

class ChatFunctionalTest(TestCase):

    def setUp(self):
        # Configuration initiale des données
        self.classe = Classe.objects.create(nom="Classe A", niveau="Terminale")
        self.salon = Salon.objects.create(nom="Salon Classe A", classe=self.classe)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.message = Message.objects.create(
            auteur=self.user,
            message="Bonjour, ceci est un message.",
            salon=self.salon
        )

    def test_salon_list_view(self):
        """Test de la vue de liste des salons"""
        response = self.client.get(reverse('chat-salon-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salon Classe A")

    def test_message_list_view(self):
        """Test de la vue de liste des messages d'un salon"""
        response = self.client.get(reverse('chat-message-list', args=[self.salon.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bonjour, ceci est un message.")

    def test_add_message_view(self):
        """Test de l'ajout d'un message via la vue"""
        response = self.client.post(reverse('chat-add-message', args=[self.salon.id]), {
            'message': 'Nouveau message'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(message="Nouveau message").exists())
