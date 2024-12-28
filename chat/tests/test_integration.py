from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe

class ChatIntegrationTest(TestCase):

    def setUp(self):
        # Configuration initiale
        self.classe = Classe.objects.create(nom="Classe A", niveau="Terminale")
        self.salon = Salon.objects.create(nom="Salon Classe A", classe=self.classe)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_add_message_to_salon(self):
        """Test d'intégration entre Message et Salon"""
        response = self.client.post(reverse('chat-add-message', args=[self.salon.id]), {
            'message': 'Nouveau message'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(message="Nouveau message").exists())
