from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Filiere, Classe, Niveau

class SchoolIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.filiere = Filiere.objects.create(nom="Sciences")
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1, filiere=self.filiere)

    def test_classe_filiere_niveau_integration(self):
        """Test d'intégration entre Classe, Filière et Niveau"""
        response = self.client.get(reverse('classe-detail', args=[self.classe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terminale 1")
        self.assertContains(response, "Sciences")

    def test_login_integration(self):
        """Test d'intégration pour la connexion utilisateur"""
        self.client.logout()
        response = self.client.post(reverse('islogin'), {
            'username': 'testuser',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect': 'admin', 'success': True, 'message': 'Vous êtes connectés!!!'}
        )

    def test_add_classe_integration(self):
        """Test d'intégration pour l'ajout d'une classe"""
        response = self.client.post(reverse('classe-add'), {
            'niveau': self.niveau.id,
            'numeroClasse': 2,
            'filiere': self.filiere.id
        })
        self.assertEqual(response.status_code, 302)  # Redirection après ajout
        self.assertTrue(Classe.objects.filter(numeroClasse=2).exists())

    def test_update_classe_integration(self):
        """Test d'intégration pour la mise à jour d'une classe"""
        response = self.client.post(reverse('classe-update', args=[self.classe.id]), {
            'niveau': self.niveau.id,
            'numeroClasse': 3,
            'filiere': self.filiere.id
        })
        self.classe.refresh_from_db()
        self.assertEqual(self.classe.numeroClasse, 3)

    def test_delete_classe_integration(self):
        """Test d'intégration pour la suppression d'une classe"""
        response = self.client.post(reverse('classe-delete', args=[self.classe.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertFalse(Classe.objects.filter(id=self.classe.id).exists())

    def test_signup_integration(self):
        """Test d'intégration pour l'inscription d'un nouvel utilisateur"""
        self.client.logout()
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newuser").exists())
