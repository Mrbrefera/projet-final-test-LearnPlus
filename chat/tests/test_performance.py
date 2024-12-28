import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe

class ChatPerformanceTest(TestCase):

    def setUp(self):
        # Configuration initiale
        self.classe = Classe.objects.create(nom="Classe A", niveau="Terminale")
        self.salon = Salon.objects.create(nom="Salon Classe A", classe=self.classe)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.message = Message.objects.create(
            auteur=self.user,
            message="Bonjour, ceci est un message.",
            salon=self.salon
        )

    def test_salon_list_performance(self):
        """Test de performance pour la vue liste des salons"""
        start_time = time.time()
        response = self.client.get(reverse('chat-salon-list'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)  # Temps de réponse < 500 ms
