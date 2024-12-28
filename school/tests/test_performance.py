import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Filiere, Classe, Niveau

class SchoolPerformanceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.filiere = Filiere.objects.create(nom="Sciences")
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1, filiere=self.filiere)

    def test_classe_list_performance(self):
        """Test de performance pour la liste des classes"""
        start_time = time.time()
        response = self.client.get(reverse('classe-list'))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)  # Temps de réponse < 500 ms

    def test_classe_detail_performance(self):
        """Test de performance pour la vue détail d'une classe"""
        start_time = time.time()
        response = self.client.get(reverse('classe-detail', args=[self.classe.id]))
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_login_performance(self):
        """Test de performance pour la connexion utilisateur"""
        self.client.logout()
        start_time = time.time()
        response = self.client.post(reverse('islogin'), {
            'username': 'testuser',
            'password': 'password123'
        }, content_type='application/json')
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(end_time - start_time < 0.5)

    def test_add_classe_performance(self):
        """Test de performance pour l'ajout d'une classe"""
        start_time = time.time()
        response = self.client.post(reverse('classe-add'), {
            'niveau': self.niveau.id,
            'numeroClasse': 2,
            'filiere': self.filiere.id
        })
        end_time = time.time()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(end_time - start_time < 0.5)

    def test_delete_classe_performance(self):
        """Test de performance pour la suppression d'une classe"""
        start_time = time.time()
        response = self.client.post(reverse('classe-delete', args=[self.classe.id]))
        end_time = time.time()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(end_time - start_time < 0.5)
